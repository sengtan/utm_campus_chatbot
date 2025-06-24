User Management
===============

This section covers comprehensive user account management for the UTM Campus Assistant system.

User Roles and Permissions
---------------------------

The system supports two primary user roles:

Student Role
~~~~~~~~~~~~

**Permissions**:

- Report facility issues
- Use AI chatbot interface
- View facility information and directions
- Book available facilities
- Track personal issue status
- Provide feedback on resolved issues

**Restrictions**:

- Cannot access admin dashboard
- Cannot manage other users
- Cannot update issue status
- Cannot access system configuration

Administrator Role
~~~~~~~~~~~~~~~~~~

**Permissions**:

- All student permissions
- Access admin dashboard
- Manage user accounts
- Update issue status and assignments
- Manage facility information
- Approve/reject facility bookings
- Access system logs and analytics
- Configure system settings
- Manage database operations

User Account Lifecycle
----------------------

User Registration
~~~~~~~~~~~~~~~~~

Students can self-register through the registration form:

1. **Registration Process**:
   
   - Username (4-20 characters, unique)
   - Email address (valid format, unique)
   - Full name
   - Student ID (optional)
   - Password (minimum 6 characters)
   - Role selection (defaults to Student)

2. **Validation Rules**:
   
   - Username must be unique
   - Email must be valid and unique
   - Student ID must be unique if provided
   - Password must meet minimum requirements

3. **Account Activation**:
   
   - Accounts are immediately active upon registration
   - Users can login immediately after registration

Admin Account Creation
~~~~~~~~~~~~~~~~~~~~~~

**Method 1: Promote Existing User**

.. code-block:: bash

   python3 -c "
   from app import app, db
   from models import User, UserRole
   with app.app_context():
       user = User.query.filter_by(username='target-username').first()
       if user:
           user.role = UserRole.ADMIN
           db.session.commit()
           print(f'User {user.username} promoted to admin')
       else:
           print('User not found')
   "

**Method 2: Database Direct Update**

.. code-block:: sql

   UPDATE users SET role = 'admin' WHERE username = 'target-username';

**Method 3: Create Admin During Registration**

Select "Admin" role during the registration process (requires existing admin approval in production).

User Account Management
-----------------------

Viewing User Accounts
~~~~~~~~~~~~~~~~~~~~~

Access user management through the admin dashboard:

1. Login as administrator
2. Navigate to "Manage Users" section
3. View user list with details:
   
   - Username and full name
   - Email address
   - Role assignment
   - Registration date
   - Last login (if tracked)
   - Account status

User Information Display
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: User Information Fields
   :widths: 25 75
   :header-rows: 1

   * - Field
     - Description
   * - ID
     - Unique user identifier
   * - Username
     - Login username
   * - Email
     - Contact email address
   * - Full Name
     - Complete user name
   * - Student ID
     - University student identifier
   * - Role
     - Student or Administrator
   * - Created At
     - Account creation timestamp

Modifying User Accounts
~~~~~~~~~~~~~~~~~~~~~~~

**Updating User Information**:

.. code-block:: python

   # Update user details
   from app import app, db
   from models import User
   
   with app.app_context():
       user = User.query.filter_by(username='username').first()
       user.email = 'new-email@utm.my'
       user.full_name = 'Updated Name'
       db.session.commit()

**Changing User Roles**:

.. code-block:: python

   # Promote to admin
   user.role = UserRole.ADMIN
   
   # Demote to student
   user.role = UserRole.STUDENT
   
   db.session.commit()

Password Management
-------------------

Password Reset (Admin)
~~~~~~~~~~~~~~~~~~~~~~

Administrators can reset user passwords:

.. code-block:: python

   from werkzeug.security import generate_password_hash
   
   with app.app_context():
       user = User.query.filter_by(username='username').first()
       new_password = 'temporary-password'
       user.password_hash = generate_password_hash(new_password)
       db.session.commit()

Password Policy
~~~~~~~~~~~~~~~

Current password requirements:

- Minimum 6 characters
- No maximum length limit
- No special character requirements (configurable)

**Recommended Security Settings**:

.. code-block:: python

   # Enhanced password policy (implementation)
   PASSWORD_MIN_LENGTH = 8
   PASSWORD_REQUIRE_UPPERCASE = True
   PASSWORD_REQUIRE_LOWERCASE = True
   PASSWORD_REQUIRE_DIGIT = True
   PASSWORD_REQUIRE_SPECIAL = True

User Activity Monitoring
------------------------

Tracking User Actions
~~~~~~~~~~~~~~~~~~~~~

Monitor user activity through:

1. **Login Tracking**:
   
   - Login timestamps
   - Failed login attempts
   - Session duration

2. **Feature Usage**:
   
   - Issue reports submitted
   - Chatbot interactions
   - Facility bookings made
   - Feedback provided

3. **Admin Actions**:
   
   - Issue status updates
   - User role changes
   - System configuration changes

Activity Logs
~~~~~~~~~~~~~

Access user activity logs:

.. code-block:: python

   # View user's issues
   user_issues = Issue.query.filter_by(user_id=user.id).all()
   
   # View user's bookings
   user_bookings = FacilityBooking.query.filter_by(user_id=user.id).all()
   
   # View chat sessions
   user_chats = ChatSession.query.filter_by(user_id=user.id).all()

User Support and Assistance
----------------------------

Common User Issues
~~~~~~~~~~~~~~~~~~

**Login Problems**:

1. Forgotten password
2. Username confusion
3. Account lockout
4. Session timeout

**Resolution Steps**:

.. code-block:: python

   # Check if user exists
   user = User.query.filter_by(email='user@utm.my').first()
   
   # Reset password
   user.password_hash = generate_password_hash('new-password')
   db.session.commit()
   
   # Verify user role
   print(f"User role: {user.role}")

Account Recovery
~~~~~~~~~~~~~~~~

**Password Recovery Process**:

1. User contacts administrator
2. Admin verifies user identity
3. Admin resets password
4. New password provided securely
5. User required to change password on next login

**Account Unlock**:

.. code-block:: python

   # If implementing account locking
   user.locked = False
   user.failed_login_attempts = 0
   db.session.commit()

Bulk User Operations
--------------------

Bulk User Import
~~~~~~~~~~~~~~~~

Import multiple users from CSV:

.. code-block:: python

   import csv
   from models import User, UserRole
   
   def import_users_from_csv(filename):
       with app.app_context():
           with open(filename, 'r') as file:
               reader = csv.DictReader(file)
               for row in reader:
                   user = User(
                       username=row['username'],
                       email=row['email'],
                       full_name=row['full_name'],
                       student_id=row.get('student_id'),
                       role=UserRole.STUDENT
                   )
                   user.password_hash = generate_password_hash(row['password'])
                   db.session.add(user)
               db.session.commit()

Bulk Role Changes
~~~~~~~~~~~~~~~~~

Change multiple user roles:

.. code-block:: python

   # Promote multiple users to admin
   admin_usernames = ['user1', 'user2', 'user3']
   
   with app.app_context():
       users = User.query.filter(User.username.in_(admin_usernames)).all()
       for user in users:
           user.role = UserRole.ADMIN
       db.session.commit()

User Data Export
~~~~~~~~~~~~~~~~

Export user data for analysis:

.. code-block:: python

   import csv
   
   def export_users_to_csv(filename):
       with app.app_context():
           users = User.query.all()
           with open(filename, 'w', newline='') as file:
               writer = csv.writer(file)
               writer.writerow(['Username', 'Email', 'Full Name', 'Role', 'Created'])
               for user in users:
                   writer.writerow([
                       user.username,
                       user.email,
                       user.full_name,
                       user.role.value,
                       user.created_at
                   ])

Security Considerations
-----------------------

Access Control
~~~~~~~~~~~~~~

**Role-Based Access Control (RBAC)**:

- Students: Limited to personal data and public features
- Admins: Full system access with audit trails

**Session Security**:

- Secure session cookies
- Session timeout after inactivity
- Protection against session hijacking

**Data Protection**:

- Password hashing with bcrypt
- Email validation and sanitization
- Input validation on all forms

User Privacy
~~~~~~~~~~~~

**Data Collection**:

- Minimal data collection principle
- Clear purpose for each data field
- User consent for data processing

**Data Retention**:

- Regular cleanup of old session data
- Archive inactive user accounts
- Secure deletion of removed accounts

Audit and Compliance
~~~~~~~~~~~~~~~~~~~~~

**Audit Trails**:

- Log all admin actions
- Track user role changes
- Monitor access patterns

**Compliance Requirements**:

- Data protection regulations
- University policies
- Security standards

User Statistics and Analytics
-----------------------------

User Metrics
~~~~~~~~~~~~

Track key user metrics:

.. code-block:: python

   # User registration trends
   from sqlalchemy import func
   from datetime import datetime, timedelta
   
   with app.app_context():
       # Users registered in last 30 days
       thirty_days_ago = datetime.utcnow() - timedelta(days=30)
       recent_users = User.query.filter(
           User.created_at >= thirty_days_ago
       ).count()
       
       # Total users by role
       students = User.query.filter_by(role=UserRole.STUDENT).count()
       admins = User.query.filter_by(role=UserRole.ADMIN).count()

Usage Analytics
~~~~~~~~~~~~~~~

Analyze user engagement:

.. code-block:: python

   # Most active users (by issues reported)
   from sqlalchemy import desc
   
   active_users = db.session.query(
       User.username,
       func.count(Issue.id).label('issue_count')
   ).join(Issue).group_by(User.id).order_by(
       desc('issue_count')
   ).limit(10).all()

Reporting
~~~~~~~~~

Generate user reports:

.. code-block:: python

   def generate_user_report():
       with app.app_context():
           report = {
               'total_users': User.query.count(),
               'students': User.query.filter_by(role=UserRole.STUDENT).count(),
               'admins': User.query.filter_by(role=UserRole.ADMIN).count(),
               'recent_registrations': User.query.filter(
                   User.created_at >= datetime.utcnow() - timedelta(days=7)
               ).count()
           }
           return report

Best Practices
--------------

User Management Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Regular Reviews**:
   
   - Review user accounts monthly
   - Remove inactive accounts
   - Audit admin permissions

2. **Security Practices**:
   
   - Enforce strong passwords
   - Monitor suspicious activity
   - Regular security training

3. **Support Procedures**:
   
   - Document common issues
   - Maintain support scripts
   - Track resolution times

Account Lifecycle Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Onboarding**:
   
   - Clear registration process
   - Welcome instructions
   - Feature orientation

2. **Maintenance**:
   
   - Regular data cleanup
   - Permission reviews
   - Performance monitoring

3. **Offboarding**:
   
   - Account deactivation process
   - Data retention policies
   - Secure data deletion

Troubleshooting User Issues
---------------------------

Common Problems and Solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**User Cannot Login**:

.. code-block:: python

   # Check if user exists and verify details
   user = User.query.filter_by(username='username').first()
   if not user:
       print("User not found")
   else:
       print(f"User found: {user.email}, Role: {user.role}")

**Permission Denied Errors**:

.. code-block:: python

   # Verify user role
   if user.role != UserRole.ADMIN:
       print("User needs admin privileges")
       user.role = UserRole.ADMIN
       db.session.commit()

**Duplicate Registration Attempts**:

.. code-block:: python

   # Check for existing users
   existing_user = User.query.filter(
       (User.username == username) | (User.email == email)
   ).first()
   
   if existing_user:
       print(f"Conflict with existing user: {existing_user.username}")

Emergency Procedures
~~~~~~~~~~~~~~~~~~~~

**Mass Password Reset**:

.. code-block:: python

   # Reset all user passwords (emergency only)
   import secrets
   
   with app.app_context():
       users = User.query.all()
       reset_log = []
       
       for user in users:
           temp_password = secrets.token_urlsafe(12)
           user.password_hash = generate_password_hash(temp_password)
           reset_log.append((user.username, temp_password))
       
       db.session.commit()
       
       # Save reset log securely
       with open('password_reset_log.txt', 'w') as f:
           for username, password in reset_log:
               f.write(f"{username}: {password}\n")

**Account Recovery**:

.. code-block:: python

   # Recover accidentally deleted admin account
   emergency_admin = User(
       username='emergency_admin',
       email='admin@utm.my',
       full_name='Emergency Administrator',
       role=UserRole.ADMIN
   )
   emergency_admin.password_hash = generate_password_hash('emergency_password')
   
   with app.app_context():
       db.session.add(emergency_admin)
       db.session.commit()