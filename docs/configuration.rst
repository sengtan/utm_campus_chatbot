Configuration and Settings
==========================

Application Configuration
-------------------------

Core Components
~~~~~~~~~~~~~~

Flask Application Stack
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Core Flask Components
   :header-rows: 1
   :widths: 30 50 20

   * - Component
     - Purpose
     - Configuration File
   * - **Flask-SQLAlchemy**
     - Database ORM and management
     - ``flask_app.py``
   * - **Flask-Login**
     - User authentication and sessions
     - ``flask_app.py``
   * - **Flask-WTF**
     - Form handling and CSRF protection
     - ``forms.py``
   * - **Flask-Bcrypt**
     - Password hashing and verification
     - ``flask_app.py``
   * - **Gunicorn**
     - WSGI HTTP server
     - Workflow configuration

Database Configuration
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Primary Database Models (models.py)
   class User(UserMixin, db.Model):
       """User account management"""
       - id: Primary key
       - username: Unique identifier
       - email: Contact information
       - role: UserRole (STUDENT/ADMIN)
       - password_hash: Bcrypt hashed password
   
   class Facility(db.Model):
       """Campus facility information"""
       - name: Facility identifier
       - category: Type classification
       - location: Physical address
       - is_bookable: Booking availability
       - capacity: Maximum occupancy
   
   class Issue(db.Model):
       """Facility issue tracking"""
       - title: Issue description
       - issue_type: Category classification
       - priority: Urgency level
       - status: Current state
       - reporter: User relationship
       - facility: Facility relationship

AI Service Configuration
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # AI Service Settings (ai_service.py)
   class AIService:
       timeout = 60  # API timeout in seconds
       
       # DeepSeek LLM Configuration
       api_url = os.environ.get("DEEPSEEK_API_URL", 
                                "http://localhost:11434/v1/chat/completions")
       model = os.environ.get("DEEPSEEK_MODEL", "deepseek-r1:7b")
       
       # Core Functions:
       - extract_entities_and_intent(): Natural language processing
       - generate_response(): Context-aware responses
       - classify_issue_from_description(): Automatic issue categorization

Security Configuration
---------------------

Authentication Settings
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # User Role Management
   class UserRole(enum.Enum):
       STUDENT = "student"  # Basic access rights
       ADMIN = "admin"      # Full system access
   
   # Password Security
   - Minimum length: 6 characters
   - Bcrypt hashing with salt
   - Session-based authentication
   - CSRF protection on all forms

Session Management
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Flask Session Configuration
   app.secret_key = os.environ.get("SESSION_SECRET")
   
   # Security Features:
   - Secure session cookies
   - CSRF token validation
   - Session timeout handling
   - User session tracking

Form Validation Rules
~~~~~~~~~~~~~~~~~~~

.. list-table:: Input Validation Rules
   :header-rows: 1
   :widths: 25 50 25

   * - Field Type
     - Validation Rules
     - Error Handling
   * - **Username**
     - 4-20 characters, unique
     - Duplicate check
   * - **Email**
     - Valid format, unique
     - Format validation
   * - **Student ID**
     - Optional, max 20 chars, unique
     - Uniqueness check
   * - **Issue Description**
     - Minimum 10 characters
     - Length validation
   * - **Facility Name**
     - 2-100 characters
     - Required field

System Workflows
---------------

Issue Management Workflow
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Student Reports Issue → AI Classification → Admin Review → Resolution → Feedback

   States:
   - REPORTED: Initial submission
   - IN_PROGRESS: Admin assigned
   - RESOLVED: Issue fixed
   - CLOSED: Feedback received

Facility Booking Workflow
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Student Request → Admin Review → Approval/Rejection → Notification

   States:
   - PENDING: Awaiting admin review
   - APPROVED: Booking confirmed
   - REJECTED: Request denied
   - CANCELLED: User cancelled

Integration Settings
-------------------

External Service Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**DeepSeek LLM Integration**:

.. code-block:: yaml

   # Required Environment Variables
   DEEPSEEK_API_URL: "http://localhost:11434/v1/chat/completions"
   DEEPSEEK_MODEL: "deepseek-r1:7b"
   
   # Fallback Configuration
   - Timeout handling: 60 seconds
   - Error recovery: Rule-based responses
   - Cache management: Facility data preloaded

**Database Integration**:

.. code-block:: yaml

   # PostgreSQL Configuration
   DATABASE_URL: "postgresql://user:pass@host:port/db"
   
   # Connection Pool Settings
   SQLALCHEMY_ENGINE_OPTIONS:
     pool_recycle: 300
     pool_pre_ping: true

Frontend Configuration
~~~~~~~~~~~~~~~~~~~~

**Static Assets**:

.. code-block:: text

   static/
   ├── css/
   │   ├── style.css          # Main stylesheet
   │   └── chatbot.css        # Chatbot specific styles
   ├── js/
   │   └── chatbot.js         # Frontend chatbot logic
   └── images/
       └── logo.png           # Application logo

**Template Structure**:

.. code-block:: text

   templates/
   ├── base.html              # Base template with Bootstrap 5
   ├── index.html             # Landing page
   ├── admin_dashboard.html   # Admin control panel
   ├── student_dashboard.html # Student interface
   ├── chatbot.html          # AI chat interface
   ├── facility_info.html    # Facility directory
   └── report_issue.html     # Issue submission form

Monitoring and Logging
---------------------

Application Logging
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Logging Configuration
   import logging
   logging.basicConfig(level=logging.DEBUG)
   
   # Log Categories:
   - Database operations
   - AI service responses
   - User authentication
   - Error tracking
   - Performance metrics

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~

**Key Metrics**:

.. list-table:: Performance Indicators
   :header-rows: 1
   :widths: 30 40 30

   * - Metric
     - Description
     - Target Value
   * - **Response Time**
     - Page load duration
     - < 2 seconds
   * - **AI Response Time**
     - Chatbot query processing
     - < 5 seconds
   * - **Database Queries**
     - Query execution time
     - < 100ms average
   * - **Memory Usage**
     - Application memory footprint
     - < 512MB
   * - **CPU Usage**
     - Processing utilization
     - < 70% average

Backup and Recovery
------------------

Database Backup Strategy
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Automated Backup (Daily)
   pg_dump utm_campus_assistant > backup_$(date +%Y%m%d).sql
   
   # Restore Procedure
   psql utm_campus_assistant < backup_YYYYMMDD.sql

Configuration Backup
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Critical Files to Backup
   - .env (environment variables)
   - instance/ (SQLite fallback)
   - static/ (custom assets)
   - templates/ (custom templates)

Environment-Specific Settings
---------------------------

Development Environment
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Development Configuration
   FLASK_ENV = "development"
   FLASK_DEBUG = True
   
   # Features:
   - Hot reload enabled
   - Detailed error pages
   - Debug toolbar available
   - SQL query logging

Production Environment
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Production Configuration
   FLASK_ENV = "production"
   FLASK_DEBUG = False
   
   # Features:
   - Error logging to files
   - Performance optimizations
   - Security hardening
   - Resource compression

Customization Options
-------------------

Theme Customization
~~~~~~~~~~~~~~~~~

.. code-block:: css

   /* Custom Theme Variables */
   :root {
     --primary-color: #007bff;
     --secondary-color: #6c757d;
     --success-color: #28a745;
     --danger-color: #dc3545;
     --warning-color: #ffc107;
   }

Feature Toggles
~~~~~~~~~~~~~

.. code-block:: python

   # Feature Configuration
   FEATURES = {
       'CHATBOT_ENABLED': True,
       'BOOKING_SYSTEM': True,
       'AI_CLASSIFICATION': True,
       'EMAIL_NOTIFICATIONS': False,
       'SMS_ALERTS': False,
   }