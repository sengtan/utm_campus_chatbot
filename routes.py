import uuid
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt
from models import User, Issue, Facility, ChatSession, ChatMessage, IssueStatus, IssueType, Priority, UserRole
from forms import LoginForm, RegistrationForm, IssueForm, FeedbackForm
from ai_service import ai_service

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == UserRole.ADMIN:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.full_name = form.full_name.data
        user.student_id = form.student_id.data if form.student_id.data else None
        user.role = UserRole(form.role.data)
        user.password_hash = hashed_password
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if current_user.role != UserRole.STUDENT:
        flash('Access denied. Students only.', 'danger')
        return redirect(url_for('index'))
    
    # Get user's recent issues
    recent_issues = Issue.query.filter_by(user_id=current_user.id)\
                             .order_by(Issue.created_at.desc())\
                             .limit(5).all()
    
    # Get statistics
    total_issues = Issue.query.filter_by(user_id=current_user.id).count()
    resolved_issues = Issue.query.filter_by(user_id=current_user.id, status=IssueStatus.RESOLVED).count()
    
    return render_template('student_dashboard.html', 
                         recent_issues=recent_issues,
                         total_issues=total_issues,
                         resolved_issues=resolved_issues)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != UserRole.ADMIN:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))
    
    # Get recent issues for admin
    recent_issues = Issue.query.order_by(Issue.created_at.desc()).limit(10).all()
    
    # Get statistics
    total_issues = Issue.query.count()
    pending_issues = Issue.query.filter_by(status=IssueStatus.REPORTED).count()
    in_progress_issues = Issue.query.filter_by(status=IssueStatus.IN_PROGRESS).count()
    resolved_issues = Issue.query.filter_by(status=IssueStatus.RESOLVED).count()
    
    return render_template('admin_dashboard.html',
                         recent_issues=recent_issues,
                         total_issues=total_issues,
                         pending_issues=pending_issues,
                         in_progress_issues=in_progress_issues,
                         resolved_issues=resolved_issues)

@app.route('/chatbot')
@login_required
def chatbot():
    # Get or create chat session
    session_id = session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['chat_session_id'] = session_id
        
        chat_session = ChatSession()
        chat_session.user_id = current_user.id
        chat_session.session_id = session_id
        db.session.add(chat_session)
        db.session.commit()
    
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get chat session
        session_id = session.get('chat_session_id')
        chat_session = ChatSession.query.filter_by(session_id=session_id).first()
        
        if not chat_session:
            return jsonify({'error': 'Chat session not found'}), 400
        
        # Process message with AI
        intent_data = ai_service.extract_entities_and_intent(user_message)
        bot_response = ai_service.generate_response(user_message, intent_data)
        
        # Save user message
        user_msg = ChatMessage()
        user_msg.session_id = chat_session.id
        user_msg.message = user_message
        user_msg.is_user = True
        user_msg.intent = intent_data.get('intent')
        user_msg.entities = intent_data.get('entities')
        db.session.add(user_msg)
        
        # Save bot response
        bot_msg = ChatMessage()
        bot_msg.session_id = chat_session.id
        bot_msg.message = bot_response
        bot_msg.is_user = False
        db.session.add(bot_msg)
        db.session.commit()
        
        return jsonify({
            'response': bot_response,
            'intent': intent_data.get('intent'),
            'entities': intent_data.get('entities')
        })
        
    except Exception as e:
        print(f"Chat API error: {e}")
        return jsonify({'error': 'Failed to process message'}), 500

@app.route('/report_issue', methods=['GET', 'POST'])
@login_required
def report_issue():
    if current_user.role != UserRole.STUDENT:
        flash('Access denied. Students only.', 'danger')
        return redirect(url_for('index'))
    
    form = IssueForm()
    if form.validate_on_submit():
        # Use AI to enhance issue classification
        ai_classification = ai_service.classify_issue_from_description(form.description.data)
        
        issue = Issue()
        issue.title = form.title.data
        issue.description = form.description.data
        issue.issue_type = IssueType(ai_classification.get('issue_type', form.issue_type.data))
        issue.priority = Priority(ai_classification.get('priority', form.priority.data))
        issue.location = form.location.data
        issue.user_id = current_user.id
        
        db.session.add(issue)
        db.session.commit()
        
        flash(f'Issue reported successfully! (ID: {issue.id})', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('report_issue.html', form=form)

@app.route('/facility_info')
@login_required
def facility_info():
    facilities = Facility.query.all()
    return render_template('facility_info.html', facilities=facilities)

@app.route('/issue/<int:issue_id>')
@login_required
def view_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    
    # Check permissions
    if current_user.role == UserRole.STUDENT and issue.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('student_dashboard'))
    
    return render_template('view_issue.html', issue=issue)

@app.route('/issue/<int:issue_id>/update_status', methods=['POST'])
@login_required
def update_issue_status(issue_id):
    if current_user.role != UserRole.ADMIN:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))
    
    issue = Issue.query.get_or_404(issue_id)
    new_status = request.form.get('status')
    admin_notes = request.form.get('admin_notes', '')
    
    if new_status in [status.value for status in IssueStatus]:
        issue.status = IssueStatus(new_status)
        issue.updated_at = datetime.utcnow()
        if admin_notes:
            issue.admin_notes = admin_notes
        if new_status == IssueStatus.RESOLVED.value:
            issue.resolved_at = datetime.utcnow()
        
        db.session.commit()
        flash('Issue status updated successfully!', 'success')
    else:
        flash('Invalid status.', 'danger')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/issue/<int:issue_id>/feedback', methods=['POST'])
@login_required
def submit_feedback(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    
    if issue.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('student_dashboard'))
    
    if issue.status != IssueStatus.RESOLVED:
        flash('Can only provide feedback for resolved issues.', 'danger')
        return redirect(url_for('view_issue', issue_id=issue_id))
    
    form = FeedbackForm()
    if form.validate_on_submit():
        issue.feedback_rating = int(form.rating.data)
        issue.feedback_comment = form.comment.data
        issue.status = IssueStatus.CLOSED
        db.session.commit()
        
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('student_dashboard'))
    
    flash('Invalid feedback data.', 'danger')
    return redirect(url_for('view_issue', issue_id=issue_id))

# Initialize some sample data
def create_sample_data():
    # Create sample facilities if none exist
    if Facility.query.count() == 0:
        facilities_data = [
            {"name": "Computer Lab 1", "category": "Laboratory", "location": "Block A, Level 2", 
             "description": "Main computer lab with 40 workstations", "is_bookable": True, "capacity": 40},
            {"name": "Library", "category": "Academic", "location": "Block B, Ground Floor", 
             "description": "Main university library", "operating_hours": "8:00 AM - 10:00 PM"},
            {"name": "Gymnasium", "category": "Sports", "location": "Sports Complex", 
             "description": "Indoor gymnasium for sports activities", "is_bookable": True},
            {"name": "Male Hostel Block C", "category": "Accommodation", "location": "Hostel Area", 
             "description": "Male student accommodation"},
            {"name": "Female Hostel Block D", "category": "Accommodation", "location": "Hostel Area", 
             "description": "Female student accommodation"},
            {"name": "Cafeteria", "category": "Dining", "location": "Student Center", 
             "description": "Main dining facility", "operating_hours": "7:00 AM - 9:00 PM"},
        ]
        
        for facility_data in facilities_data:
            facility = Facility()
            for key, value in facility_data.items():
                setattr(facility, key, value)
            db.session.add(facility)
        
        db.session.commit()
        print("Sample facilities created")

# Refresh AI service facilities cache when needed
@app.route('/admin/refresh_cache')
@login_required
def refresh_cache():
    if current_user.role != UserRole.ADMIN:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    ai_service.load_facilities()
    flash('AI service cache refreshed successfully!', 'success')
    return redirect(url_for('admin_dashboard'))
