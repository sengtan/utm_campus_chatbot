import uuid
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt
from models import User, Issue, Facility, ChatSession, ChatMessage, IssueStatus, IssueType, Priority, UserRole, FacilityBooking, BookingStatus
from forms import LoginForm, RegistrationForm, IssueForm, FeedbackForm, BookingForm, BookingManagementForm, FacilityForm, FacilityManagementForm
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
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
    
    # Get user's recent bookings
    recent_bookings = FacilityBooking.query.filter_by(user_id=current_user.id)\
                                          .order_by(FacilityBooking.created_at.desc())\
                                          .limit(3).all()
    
    # Get statistics
    total_issues = Issue.query.filter_by(user_id=current_user.id).count()
    resolved_issues = Issue.query.filter_by(user_id=current_user.id, status=IssueStatus.RESOLVED).count()
    
    return render_template('student_dashboard.html', 
                         recent_issues=recent_issues,
                         recent_bookings=recent_bookings,
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
    
    # Get recent bookings for admin
    recent_bookings = FacilityBooking.query.order_by(FacilityBooking.created_at.desc()).limit(5).all()
    
    # Get statistics
    total_issues = Issue.query.count()
    pending_issues = Issue.query.filter_by(status=IssueStatus.REPORTED).count()
    in_progress_issues = Issue.query.filter_by(status=IssueStatus.IN_PROGRESS).count()
    resolved_issues = Issue.query.filter_by(status=IssueStatus.RESOLVED).count()
    
    # Get booking statistics
    total_bookings = FacilityBooking.query.count()
    pending_bookings = FacilityBooking.query.filter_by(status=BookingStatus.PENDING).count()
    approved_bookings = FacilityBooking.query.filter_by(status=BookingStatus.APPROVED).count()
    
    return render_template('admin_dashboard.html',
                         recent_issues=recent_issues,
                         recent_bookings=recent_bookings,
                         total_issues=total_issues,
                         pending_issues=pending_issues,
                         in_progress_issues=in_progress_issues,
                         resolved_issues=resolved_issues,
                         total_bookings=total_bookings,
                         pending_bookings=pending_bookings,
                         approved_bookings=approved_bookings)

@app.route('/chatbot')
@login_required
def chatbot():
    # Get or create chat session
    session_id = session.get('chat_session_id')
    chat_session = None
    if session_id:
        chat_session = ChatSession.query.filter_by(session_id=session_id).first()
    if not session_id or not chat_session:
        session_id = str(uuid.uuid4())
        session['chat_session_id'] = session_id

        chat_session = ChatSession()
        chat_session.user_id = current_user.id
        chat_session.session_id = session_id
        db.session.add(chat_session)
        db.session.commit()
    
    # Get context from URL parameters
    facility = request.args.get('facility', '')
    location = request.args.get('location', '')
    context = request.args.get('context', '')
    initial_message = request.args.get('message', '')
    
    return render_template('chatbot.html', 
                         context_facility=facility,
                         context_location=location, 
                         context_type=context,
                         initial_message=initial_message)

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
    
    # Pre-fill form if URL parameters are provided
    facility_name = request.args.get('facility', '')
    location = request.args.get('location', '')
    context = request.args.get('context', '')
    from_page = request.args.get('from_page', '')
    
    if location:
        form.location.data = location
    
    # Add context information for better user experience
    context_info = ''
    if context == 'directions' and from_page == 'facility_directions':
        context_info = f'Issue reported from directions page for {facility_name}'
        # Pre-fill title with context if facility name is available
        if facility_name and not form.title.data:
            form.title.data = f'Issue with {facility_name}'
    elif context == 'facility_info' and from_page == 'facility_info':
        context_info = f'Issue reported from facility info page for {facility_name}'
        # Pre-fill title with context if facility name is available
        if facility_name and not form.title.data:
            form.title.data = f'Issue with {facility_name}'
    
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
    
    return render_template('report_issue.html', form=form, context_info=context_info)

@app.route('/facility_info')
def facility_info():
    """Display all facilities with search and filter options"""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Facility.query.filter(Facility.is_active == True)
    
    if search:
        query = query.filter(
            Facility.name.ilike(f'%{search}%') |
            Facility.location.ilike(f'%{search}%') |
            Facility.description.ilike(f'%{search}%')
        )
    
    if category:
        query = query.filter(Facility.category == category)
    
    facilities = query.all()
    
    # Get unique categories for filter dropdown
    categories = db.session.query(Facility.category).distinct().filter(Facility.is_active == True).all()
    categories = [cat[0] for cat in categories]
    
    return render_template('facility_info.html', 
                         facilities=facilities, 
                         categories=categories,
                         search=search,
                         selected_category=category)

@app.route('/directions/<int:facility_id>')
@login_required
def facility_directions(facility_id):
    facility = Facility.query.get_or_404(facility_id)
    
    # Create detailed step-by-step directions based on facility location
    directions_data = get_facility_directions(facility)
    
    return render_template('directions.html', 
                         facility=facility, 
                         directions=directions_data)

def get_facility_directions(facility):
    """Generate detailed directions for a specific facility"""
    
    # Base directions for all facilities starting from main entrance
    base_steps = [
        {
            'step': 1,
            'instruction': 'Enter UTM campus via the main entrance gate',
            'detail': 'Show your student/staff ID at the security checkpoint',
            'landmark': 'Main Gate Security Post'
        },
        {
            'step': 2, 
            'instruction': 'Head towards the Faculty of Computing area',
            'detail': 'Walk straight along the main campus road towards the center of campus',
            'landmark': 'Pass by Arked Angkasa food court on your right'
        }
    ]
    
    # Facility-specific directions
    facility_specific = {
        'Activity Learning Lab': [
            {
                'step': 3,
                'instruction': 'Locate the N28 building (Faculty of Computing)',
                'detail': 'Look for the large multi-story building with "Faculty of Computing" signage',
                'landmark': 'N28 Building - Faculty of Computing'
            },
            {
                'step': 4,
                'instruction': 'Enter N28 building and take elevator to Level 5',
                'detail': 'Use the main entrance and elevator banks on the ground floor',
                'landmark': 'Level 5, N28 Building'
            },
            {
                'step': 5,
                'instruction': 'Find the Activity Learning Lab',
                'detail': 'Look for room signage indicating Activity Learning Lab',
                'landmark': 'Activity Learning Lab - Level 5'
            }
        ],
        'Lecture Room Type A': [
            {
                'step': 3,
                'instruction': 'Locate the N28A building',
                'detail': 'Main Faculty of Computing building with lecture halls',
                'landmark': 'N28A Building entrance'
            },
            {
                'step': 4,
                'instruction': 'Look for Lecture Room Type A signage',
                'detail': '2 rooms available in N28A, 7 rooms in N28 building',
                'landmark': 'Lecture Room Type A'
            }
        ],
        'Lecture Room Type B': [
            {
                'step': 3,
                'instruction': 'Go to Level 1 of N28 or N28A building',
                'detail': 'Ground floor level for easy access',
                'landmark': 'Level 1, N28/N28A Buildings'
            },
            {
                'step': 4,
                'instruction': 'Find Lecture Room Type B',
                'detail': 'Look for room directory or signage on Level 1',
                'landmark': 'Lecture Room Type B - Level 1'
            }
        ],
        'Computer Lab': [
            {
                'step': 3,
                'instruction': 'Enter either N28 or N28A building',
                'detail': '12 computer labs distributed across both buildings',
                'landmark': 'N28/N28A Computer Lab areas'
            },
            {
                'step': 4,
                'instruction': 'Look for "Computer Lab" signage',
                'detail': 'Check building directory for specific lab locations',
                'landmark': 'Computer Lab entrance'
            }
        ],
        'CCNP Network Lab': [
            {
                'step': 3,
                'instruction': 'Enter N28 building',
                'detail': 'Main Faculty of Computing building',
                'landmark': 'N28 Building entrance'
            },
            {
                'step': 4,
                'instruction': 'Take elevator to Level 4',
                'detail': 'Specialized networking laboratory on 4th floor',
                'landmark': 'Level 4, N28 Building'
            },
            {
                'step': 5,
                'instruction': 'Find CCNP Network Lab',
                'detail': 'Look for networking lab signage and specialized equipment',
                'landmark': 'CCNP Network Lab - Level 4'
            }
        ],
        'Tutorial Room': [
            {
                'step': 3,
                'instruction': 'Go to N28A building',
                'detail': 'Main Faculty of Computing building',
                'landmark': 'N28A Building entrance'
            },
            {
                'step': 4,
                'instruction': 'Stay on Level 1 (Ground Floor)',
                'detail': '6 tutorial rooms available on this level',
                'landmark': 'Level 1, N28A Building'
            },
            {
                'step': 5,
                'instruction': 'Find Tutorial Room',
                'detail': 'Small rooms designed for group discussions',
                'landmark': 'Tutorial Room - Level 1'
            }
        ],
        'Meeting Room': [
            {
                'step': 3,
                'instruction': 'Check both N28A and N28 buildings',
                'detail': '2 meeting rooms in N28A, 1 meeting room in N28',
                'landmark': 'N28A/N28 Building meeting areas'
            },
            {
                'step': 4,
                'instruction': 'Look for "Meeting Room" signage',
                'detail': 'Professional meeting spaces with presentation equipment',
                'landmark': 'Meeting Room entrance'
            }
        ],
        'Kejora Hall': [
            {
                'step': 3,
                'instruction': 'Enter N28A building',
                'detail': 'Main Faculty of Computing building',
                'landmark': 'N28A Building main entrance'
            },
            {
                'step': 4,
                'instruction': 'Look for Kejora Hall signage',
                'detail': 'Large seminar hall - the biggest venue in the faculty',
                'landmark': 'Kejora Hall entrance'
            }
        ],
        'Discussion Room': [
            {
                'step': 3,
                'instruction': 'Enter N28A building',
                'detail': 'Main Faculty of Computing building',
                'landmark': 'N28A Building entrance'
            },
            {
                'step': 4,
                'instruction': 'Take elevator to Level 2',
                'detail': 'Second floor of the building',
                'landmark': 'Level 2, N28A Building'
            },
            {
                'step': 5,
                'instruction': 'Find Discussion Room',
                'detail': '3 small discussion rooms available on this level',
                'landmark': 'Discussion Room - Level 2'
            }
        ]
    }
    
    # Combine base steps with facility-specific steps
    all_steps = base_steps + facility_specific.get(facility.name, [])
    
    return {
        'steps': all_steps,
        'total_time': '5-10 minutes walking',
        'difficulty': 'Easy',
        'accessibility': 'Wheelchair accessible via elevators',
        'map_markers': get_map_markers(facility)
    }

def get_map_markers(facility):
    """Generate map markers for the route visualization"""
    return {
        'start': {'lat': 1.5586, 'lng': 103.6383, 'label': 'Main Entrance'},
        'waypoints': [
            {'lat': 1.5590, 'lng': 103.6385, 'label': 'Arked Angkasa'},
            {'lat': 1.5594, 'lng': 103.6387, 'label': 'Faculty of Computing'}
        ],
        'destination': {'lat': 1.5596, 'lng': 103.6388, 'label': facility.name}
    }

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

# Facility Booking Routes
@app.route('/book_facility', methods=['GET', 'POST'])
@login_required
def book_facility():
    """Book a facility"""
    form = BookingForm()
    
    # Populate facility choices
    facilities = Facility.query.filter_by(is_bookable=True).all()
    form.facility_id.choices = [(f.id, f.name) for f in facilities]
    
    # Handle facility pre-selection from URL parameter
    facility_name = request.args.get('facility')
    if facility_name:
        selected_facility = Facility.query.filter_by(name=facility_name, is_bookable=True).first()
        if selected_facility:
            form.facility_id.data = selected_facility.id
    
    # Pre-select facility if specified in URL parameter
    facility_name = request.args.get('facility')
    if facility_name and request.method == 'GET':
        for facility in facilities:
            if facility.name == facility_name:
                form.facility_id.data = facility.id
                break
    
    if form.validate_on_submit():
        # Check for conflicts
        existing_booking = FacilityBooking.query.filter_by(
            facility_id=form.facility_id.data,
            booking_date=form.booking_date.data
        ).filter(
            FacilityBooking.start_hour < form.end_hour.data,
            FacilityBooking.end_hour > form.start_hour.data,
            FacilityBooking.status.in_([BookingStatus.PENDING, BookingStatus.APPROVED])
        ).first()
        
        if existing_booking:
            flash('Time slot is already booked. Please choose a different time.', 'error')
        else:
            booking = FacilityBooking(
                facility_id=form.facility_id.data,
                user_id=current_user.id,
                booking_date=form.booking_date.data,
                start_hour=form.start_hour.data,
                end_hour=form.end_hour.data,
                purpose=form.purpose.data
            )
            db.session.add(booking)
            db.session.commit()
            flash('Booking request submitted successfully!', 'success')
            return redirect(url_for('my_bookings'))
    
    return render_template('book_facility.html', form=form, facilities=facilities)

@app.route('/my_bookings')
@login_required
def my_bookings():
    """View user's bookings"""
    bookings = FacilityBooking.query.filter_by(user_id=current_user.id).order_by(
        FacilityBooking.booking_date.desc(),
        FacilityBooking.start_hour.desc()
    ).all()
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/facility_schedule/<int:facility_id>')
@login_required
def facility_schedule(facility_id):
    """View facility booking schedule"""
    facility = Facility.query.get_or_404(facility_id)
    from datetime import date, timedelta
    
    # Get bookings for the next 30 days
    start_date = date.today()
    end_date = start_date + timedelta(days=30)
    
    bookings = FacilityBooking.query.filter(
        FacilityBooking.facility_id == facility_id,
        FacilityBooking.booking_date >= start_date,
        FacilityBooking.booking_date <= end_date,
        FacilityBooking.status.in_([BookingStatus.PENDING, BookingStatus.APPROVED])
    ).order_by(FacilityBooking.booking_date, FacilityBooking.start_hour).all()
    
    return render_template('facility_schedule.html', facility=facility, bookings=bookings)

@app.route('/manage_bookings')
@login_required
def manage_bookings():
    """Admin view to manage all bookings"""
    if current_user.role != UserRole.ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    
    bookings = FacilityBooking.query.order_by(
        FacilityBooking.booking_date.desc(),
        FacilityBooking.start_hour.desc()
    ).all()
    
    return render_template('manage_bookings.html', bookings=bookings)

@app.route('/update_booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def update_booking(booking_id):
    """Update booking status (admin only)"""
    if current_user.role != UserRole.ADMIN:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    
    booking = FacilityBooking.query.get_or_404(booking_id)
    form = BookingManagementForm()
    
    if form.validate_on_submit():
        booking.status = BookingStatus(form.status.data)
        booking.admin_notes = form.admin_notes.data
        db.session.commit()
        flash('Booking updated successfully!', 'success')
        return redirect(url_for('manage_bookings'))

@app.route('/reset_database', methods=['POST'])
@login_required
def reset_database():
    """Reset database to initial state (admin only)"""
    if current_user.role != UserRole.ADMIN:
        flash('Admin access required.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Clear all data except admin users
        db.session.query(ChatMessage).delete()
        db.session.query(ChatSession).delete()
        db.session.query(FacilityBooking).delete()
        db.session.query(Issue).delete()
        
        # Keep admin users, remove only student users
        student_users = User.query.filter_by(role=UserRole.STUDENT).all()
        for user in student_users:
            db.session.delete(user)
        
        db.session.commit()
        
        # Recreate sample facilities if they don't exist
        if Facility.query.count() == 0:
            return redirect(url_for('create_sample_data'))
        
        flash('Database reset successfully! All user data, issues, and bookings have been cleared.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error resetting database: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))
