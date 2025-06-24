First Setup Guide
=================

This guide walks through the initial setup after installing the UTM Campus Assistant system.

Initial Configuration
----------------------

After successful installation, complete these essential setup steps:

1. Create Administrator Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create the first admin user:

.. code-block:: bash

   # Register through the web interface first, then promote to admin
   python3 -c "
   from app import app, db
   from models import User, UserRole
   with app.app_context():
       # Find your registered user
       user = User.query.filter_by(username='your-username').first()
       if user:
           user.role = UserRole.ADMIN
           db.session.commit()
           print(f'User {user.username} promoted to admin')
       else:
           print('User not found - please register first')
   "

2. Initialize Facility Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add sample facility data or import your facilities:

.. code-block:: bash

   # Load sample facilities
   python3 -c "from routes import create_sample_data; create_sample_data()"

3. Configure AI Service
~~~~~~~~~~~~~~~~~~~~~~~

Set up the chatbot AI service (optional):

.. code-block:: bash

   # Test AI connectivity
   curl -X POST http://localhost:11434/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"deepseek-r1:7b","messages":[{"role":"user","content":"Hello"}]}'

System Verification
-------------------

Test Core Features
~~~~~~~~~~~~~~~~~~

1. **User Registration and Login**
   - Register a test student account
   - Login with both student and admin credentials
   - Verify role-based access

2. **Facility Management**
   - Browse facility information
   - Test facility search and filtering
   - Verify facility details display correctly

3. **Issue Reporting**
   - Submit a test issue report
   - Verify admin can view and update issues
   - Test issue status workflow

4. **Booking System**
   - Attempt to book an available facility
   - Verify booking appears in admin dashboard
   - Test booking approval process

5. **Chatbot Interface**
   - Access the chatbot page
   - Send test messages
   - Verify responses (may show fallback if AI not configured)

Database Health Check
~~~~~~~~~~~~~~~~~~~~~

Verify database setup:

.. code-block:: bash

   python3 -c "
   from app import app, db
   from models import User, Facility, Issue
   with app.app_context():
       print(f'Users: {User.query.count()}')
       print(f'Facilities: {Facility.query.count()}')
       print(f'Issues: {Issue.query.count()}')
       print('Database health: OK')
   "

Essential Settings
------------------

Configure Security
~~~~~~~~~~~~~~~~~~

1. **Session Security**
   
   Ensure secure session configuration:
   
   .. code-block:: bash
   
      # Verify session secret is set
      python3 -c "
      from app import app
      if app.secret_key:
          print('Session secret: Configured')
      else:
          print('WARNING: Session secret not set')
      "

2. **Password Security**
   
   Current password requirements:
   - Minimum 6 characters
   - Case-insensitive
   - No special characters required

System Monitoring
~~~~~~~~~~~~~~~~~

1. **Log Monitoring**
   
   Monitor application logs:
   
   .. code-block:: bash
   
      # Watch logs in real-time
      tail -f utm_campus.log

2. **Performance Monitoring**
   
   Check system performance:
   
   .. code-block:: bash
   
      # Monitor process resources
      ps aux | grep gunicorn

User Onboarding
---------------

Create Initial Users
~~~~~~~~~~~~~~~~~~~~

Set up initial user accounts:

1. **Administrator Accounts**
   - IT Support Admin
   - Facility Manager Admin
   - System Administrator

2. **Test Student Accounts**
   - Create sample student accounts for testing
   - Verify student functionality

Access Instructions
~~~~~~~~~~~~~~~~~~~

Provide users with access information:

- **Application URL**: http://your-domain:5000
- **Registration Process**: Self-registration available
- **Support Contact**: it-support@utm.my

Data Import
-----------

Facility Data Import
~~~~~~~~~~~~~~~~~~~~

Import existing facility data:

.. code-block:: python

   # Example facility import script
   from app import app, db
   from models import Facility
   
   facilities_data = [
       {
           'name': 'Computer Lab 1',
           'category': 'Laboratory',
           'location': 'Block A, Level 2',
           'description': 'Main computer lab with 40 workstations',
           'is_bookable': True,
           'capacity': 40,
           'operating_hours': '8:00 AM - 6:00 PM'
       },
       # Add more facilities...
   ]
   
   with app.app_context():
       for facility_data in facilities_data:
           facility = Facility(**facility_data)
           db.session.add(facility)
       db.session.commit()

User Data Import
~~~~~~~~~~~~~~~~

Import user accounts from existing systems:

.. code-block:: python

   import csv
   from models import User, UserRole
   from werkzeug.security import generate_password_hash
   
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

Backup Setup
------------

Initial Backup
~~~~~~~~~~~~~~

Create first system backup:

.. code-block:: bash

   # Create backup directory
   mkdir -p backups
   
   # Backup database
   cp instance/utm_campus.db backups/utm_campus_$(date +%Y%m%d_%H%M%S).db
   
   # Backup configuration
   tar czf backups/config_backup_$(date +%Y%m%d).tar.gz *.py docs/ static/ templates/

Automated Backup Schedule
~~~~~~~~~~~~~~~~~~~~~~~~~

Set up regular backups:

.. code-block:: bash

   # Add to crontab for daily backups at 2 AM
   0 2 * * * /path/to/backup_script.sh

Integration Setup
-----------------

Email Notifications
~~~~~~~~~~~~~~~~~~~

Configure email settings:

.. code-block:: bash

   # Email configuration variables
   MAIL_SERVER=smtp.utm.my
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=utm-campus@utm.my
   MAIL_PASSWORD=your-email-password

External Services
~~~~~~~~~~~~~~~~~

Configure external integrations:

1. **AI Service Integration**
   - DeepSeek LLM setup
   - API key configuration
   - Service health monitoring

2. **Database Integration**
   - External database connections
   - Backup services
   - Monitoring tools

Quality Assurance
-----------------

System Testing
~~~~~~~~~~~~~~

Run comprehensive tests:

.. code-block:: bash

   # Test database connectivity
   python3 -c "
   from app import app, db
   with app.app_context():
       try:
           db.engine.connect()
           print('✓ Database connection successful')
       except Exception as e:
           print(f'✗ Database error: {e}')
   "
   
   # Test web server response
   curl -I http://localhost:5000/
   
   # Test AI service (if configured)
   curl -s http://localhost:11434/api/version

Performance Testing
~~~~~~~~~~~~~~~~~~~

Validate system performance:

.. code-block:: bash

   # Monitor response times
   time curl -s http://localhost:5000/ > /dev/null
   
   # Check memory usage
   ps aux | grep gunicorn | awk '{sum+=$6} END {print "Memory usage: " sum/1024 " MB"}'

Documentation
-------------

Create Documentation
~~~~~~~~~~~~~~~~~~~~

Document your setup:

1. **System Configuration**
   - Environment variables used
   - Custom configurations
   - Integration details

2. **User Guides**
   - Student user guide
   - Admin procedures
   - Support contacts

3. **Operational Procedures**
   - Backup procedures
   - Update processes
   - Troubleshooting guides

Training Materials
~~~~~~~~~~~~~~~~~~

Prepare training resources:

1. **Administrator Training**
   - Dashboard navigation
   - User management
   - Issue handling procedures

2. **User Training**
   - Registration process
   - Feature overview
   - Support procedures

Go-Live Checklist
-----------------

Pre-Launch Verification
~~~~~~~~~~~~~~~~~~~~~~~

Complete this checklist before going live:

.. list-table:: Go-Live Checklist
   :widths: 5 95
   :header-rows: 1

   * - ✓
     - Task
   * - ☐
     - Admin account created and tested
   * - ☐
     - Facility data loaded and verified
   * - ☐
     - User registration process tested
   * - ☐
     - Issue reporting workflow verified
   * - ☐
     - Booking system functional
   * - ☐
     - Security settings configured
   * - ☐
     - Backup system operational
   * - ☐
     - Monitoring tools active
   * - ☐
     - Documentation complete
   * - ☐
     - User training conducted
   * - ☐
     - Support procedures established

Launch Day Tasks
~~~~~~~~~~~~~~~~

Execute these tasks on launch day:

1. **System Activation**
   - Start all services
   - Verify system health
   - Monitor initial usage

2. **User Communication**
   - Send launch announcements
   - Provide access instructions
   - Share support contacts

3. **Monitoring**
   - Watch system performance
   - Monitor error logs
   - Track user registrations

Post-Launch Support
-------------------

First Week Activities
~~~~~~~~~~~~~~~~~~~~~

1. **Daily Monitoring**
   - Check system health
   - Review user feedback
   - Monitor performance metrics

2. **User Support**
   - Respond to user queries
   - Resolve technical issues
   - Gather feedback

3. **System Optimization**
   - Identify performance bottlenecks
   - Optimize configurations
   - Plan improvements

Ongoing Maintenance
~~~~~~~~~~~~~~~~~~~

Establish regular maintenance:

1. **Weekly Tasks**
   - Review system logs
   - Update facility information
   - Generate usage reports

2. **Monthly Tasks**
   - System updates
   - Security reviews
   - Performance analysis

3. **Quarterly Tasks**
   - Major feature updates
   - Security audits
   - Disaster recovery testing

Next Steps
----------

After completing the initial setup:

1. Review the :doc:`../admin-dashboard/index` for daily operations
2. Study :doc:`../user-management/index` for user administration
3. Explore :doc:`../monitoring/index` for system monitoring
4. Set up :doc:`../backup/index` procedures

Support Resources
-----------------

If you need assistance during setup:

- **Documentation**: This admin manual
- **Email Support**: it-support@utm.my
- **Emergency Contact**: +60-7-553-4100
- **Online Resources**: System GitHub repository