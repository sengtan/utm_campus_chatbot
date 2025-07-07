API Reference
=============

This section provides detailed technical documentation for all components, functions, and APIs in the UTM Campus Assistant Chatbot system.

Core Application Structure
--------------------------

Flask Application (main.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:

Flask App Configuration (flask_app.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: flask_app
   :members:
   :undoc-members:
   :show-inheritance:

**Key Components:**

.. code-block:: python

   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy
   from flask_login import LoginManager
   from flask_bcrypt import Bcrypt
   
   # Application Factory Pattern
   app = Flask(__name__)
   db = SQLAlchemy(model_class=Base)
   login_manager = LoginManager()
   bcrypt = Bcrypt()

Database Models (models.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: models
   :members:
   :undoc-members:
   :show-inheritance:

User Model
^^^^^^^^^

.. autoclass:: models.User
   :members:
   :undoc-members:
   :show-inheritance:

**Database Schema:**

.. code-block:: sql

   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       username VARCHAR(80) UNIQUE NOT NULL,
       email VARCHAR(120) UNIQUE NOT NULL,
       password_hash VARCHAR(256) NOT NULL,
       role VARCHAR(20) NOT NULL DEFAULT 'student',
       full_name VARCHAR(100) NOT NULL,
       student_id VARCHAR(20) UNIQUE,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

Facility Model
^^^^^^^^^^^^^

.. autoclass:: models.Facility
   :members:
   :undoc-members:
   :show-inheritance:

**Database Schema:**

.. code-block:: sql

   CREATE TABLE facilities (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       category VARCHAR(50) NOT NULL,
       location VARCHAR(200) NOT NULL,
       description TEXT,
       is_bookable BOOLEAN DEFAULT FALSE,
       is_active BOOLEAN DEFAULT TRUE,
       capacity INTEGER,
       operating_hours VARCHAR(100),
       contact_info VARCHAR(200),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

Issue Model
^^^^^^^^^^

.. autoclass:: models.Issue
   :members:
   :undoc-members:
   :show-inheritance:

**Database Schema:**

.. code-block:: sql

   CREATE TABLE issues (
       id SERIAL PRIMARY KEY,
       title VARCHAR(200) NOT NULL,
       description TEXT NOT NULL,
       issue_type VARCHAR(20) NOT NULL,
       priority VARCHAR(10) DEFAULT 'medium',
       status VARCHAR(20) DEFAULT 'reported',
       location VARCHAR(200) NOT NULL,
       user_id INTEGER REFERENCES users(id),
       facility_id INTEGER REFERENCES facilities(id),
       assigned_to INTEGER REFERENCES users(id),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       resolved_at TIMESTAMP,
       admin_notes TEXT,
       feedback_rating INTEGER,
       feedback_comment TEXT
   );

FacilityBooking Model
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: models.FacilityBooking
   :members:
   :undoc-members:
   :show-inheritance:

**Database Schema:**

.. code-block:: sql

   CREATE TABLE facility_bookings (
       id SERIAL PRIMARY KEY,
       facility_id INTEGER REFERENCES facilities(id),
       user_id INTEGER REFERENCES users(id),
       booking_date DATE NOT NULL,
       start_hour INTEGER NOT NULL,
       end_hour INTEGER NOT NULL,
       purpose VARCHAR(200),
       status VARCHAR(20) DEFAULT 'pending',
       admin_notes TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

Route Handlers (routes.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: routes
   :members:
   :undoc-members:
   :show-inheritance:

Authentication Routes
^^^^^^^^^^^^^^^^^^^^

.. autofunction:: routes.login
.. autofunction:: routes.register
.. autofunction:: routes.logout

**API Endpoints:**

.. list-table:: Authentication API
   :header-rows: 1
   :widths: 15 15 20 50

   * - Method
     - Endpoint
     - Parameters
     - Description
   * - GET
     - ``/login``
     - None
     - Display login form
   * - POST
     - ``/login``
     - username, password
     - Authenticate user and create session
   * - GET
     - ``/register``
     - None
     - Display registration form
   * - POST
     - ``/register``
     - User form data
     - Create new user account
   * - POST
     - ``/logout``
     - None
     - End user session

Dashboard Routes
^^^^^^^^^^^^^^^

.. autofunction:: routes.student_dashboard
.. autofunction:: routes.admin_dashboard

Facility Management Routes
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: routes.facility_info
.. autofunction:: routes.facility_directions
.. autofunction:: routes.book_facility
.. autofunction:: routes.facility_schedule

Issue Management Routes
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: routes.report_issue
.. autofunction:: routes.view_issue
.. autofunction:: routes.update_issue_status
.. autofunction:: routes.submit_feedback

Chatbot Routes
^^^^^^^^^^^^^

.. autofunction:: routes.chatbot
.. autofunction:: routes.chat_api

Form Definitions (forms.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: forms
   :members:
   :undoc-members:
   :show-inheritance:

User Forms
^^^^^^^^^

.. autoclass:: forms.LoginForm
   :members:
   :undoc-members:

.. autoclass:: forms.RegistrationForm
   :members:
   :undoc-members:

**Form Validation Rules:**

.. code-block:: python

   class RegistrationForm(FlaskForm):
       username = StringField('Username', 
                              validators=[DataRequired(), Length(min=4, max=20)])
       email = StringField('Email', 
                          validators=[DataRequired(), Email()])
       full_name = StringField('Full Name', 
                              validators=[DataRequired(), Length(min=2, max=100)])
       student_id = StringField('Student ID', 
                               validators=[Length(max=20)])
       password = PasswordField('Password', 
                               validators=[DataRequired(), Length(min=6)])
       password2 = PasswordField('Confirm Password', 
                                validators=[DataRequired(), EqualTo('password')])

Facility Forms
^^^^^^^^^^^^^

.. autoclass:: forms.IssueForm
   :members:
   :undoc-members:

.. autoclass:: forms.BookingForm
   :members:
   :undoc-members:

.. autoclass:: forms.FacilityForm
   :members:
   :undoc-members:

AI Service (ai_service.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: ai_service
   :members:
   :undoc-members:
   :show-inheritance:

Core AI Functions
^^^^^^^^^^^^^^^^

.. autoclass:: ai_service.AIService
   :members:
   :undoc-members:

**Key Methods:**

.. automethod:: ai_service.AIService.extract_entities_and_intent
.. automethod:: ai_service.AIService.generate_response
.. automethod:: ai_service.AIService.classify_issue_from_description

**API Integration:**

.. code-block:: python

   # DeepSeek API Configuration
   class AIService:
       def __init__(self):
           self.api_url = os.environ.get("DEEPSEEK_API_URL", 
                                        "http://localhost:11434/v1/chat/completions")
           self.model = os.environ.get("DEEPSEEK_MODEL", "deepseek-r1:7b")
           self.timeout = 60
           
       def _make_api_request(self, messages):
           """Make request to DeepSeek LLM API"""
           payload = {
               "model": self.model,
               "messages": messages,
               "temperature": 0.7,
               "max_tokens": 1000
           }

Entity Extraction
^^^^^^^^^^^^^^^^

**Intent Classification:**

.. code-block:: python

   # Supported Intent Types
   INTENT_TYPES = {
       'facility_info': 'Request information about facilities',
       'facility_directions': 'Request directions to facilities', 
       'issue_report': 'Report facility issues',
       'booking_inquiry': 'Facility booking questions',
       'general_query': 'General campus questions',
       'greeting': 'Conversational greetings',
       'unknown': 'Unrecognized intent'
   }

**Entity Types:**

.. code-block:: python

   # Extracted Entity Structure
   entities = {
       'facilities': ['Library', 'Lab A', 'Sports Complex'],
       'issue_types': ['electrical', 'hygiene', 'equipment'],
       'locations': ['Block A', 'Level 2', 'Room 101'],
       'time_references': ['today', 'tomorrow', 'next week'],
       'priorities': ['urgent', 'high', 'medium', 'low']
   }

Frontend JavaScript API
-----------------------

Chatbot Interface (static/js/chatbot.js)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**ChatBot Class:**

.. code-block:: javascript

   class ChatBot {
       constructor() {
           this.chatContainer = document.getElementById('chat-container');
           this.messageInput = document.getElementById('message-input');
           this.sendButton = document.getElementById('send-button');
           this.initializeEventListeners();
       }
       
       // Core Methods
       async sendMessage()
       async sendToAPI(message, history)
       addUserMessage(message)
       addBotMessage(message, intent, entities)
       formatBotMessage(message)
   }

**API Communication:**

.. code-block:: javascript

   async sendToAPI(message, history) {
       const response = await fetch('/chat', {
           method: 'POST',
           headers: {
               'Content-Type': 'application/json',
               'X-CSRFToken': this.getCSRFToken()
           },
           body: JSON.stringify({
               message: message,
               history: history
           })
       });
       return await response.json();
   }

**Message Formatting:**

.. code-block:: javascript

   formatBotMessage(message) {
       // Handle markdown-style formatting
       return message
           .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
           .replace(/\*(.*?)\*/g, '<em>$1</em>')
           .replace(/`(.*?)`/g, '<code>$1</code>')
           .replace(/\n/g, '<br>');
   }

REST API Endpoints
-----------------

Chat API
~~~~~~~

**Endpoint:** ``POST /chat``

**Request Format:**

.. code-block:: json

   {
       "message": "Where is the library?",
       "history": [
           {"user": "Hello", "bot": "Hi! How can I help you?"}
       ]
   }

**Response Format:**

.. code-block:: json

   {
       "response": "The library is located in Block C, Level 1...",
       "intent": "facility_directions",
       "entities": {
           "facilities": ["library"],
           "locations": ["Block C", "Level 1"]
       },
       "status": "success"
   }

**Error Response:**

.. code-block:: json

   {
       "error": "AI service unavailable",
       "fallback_response": "I'm sorry, I'm having trouble...",
       "status": "error"
   }

Facility API
~~~~~~~~~~~

**Get Facilities:** ``GET /facilities``

**Response:**

.. code-block:: json

   {
       "facilities": [
           {
               "id": 1,
               "name": "Main Library",
               "category": "Academic",
               "location": "Block C, Level 1",
               "is_bookable": true,
               "capacity": 200,
               "operating_hours": "8:00 AM - 10:00 PM"
           }
       ]
   }

**Get Facility Details:** ``GET /facility/<id>``

**Facility Booking:** ``POST /book-facility``

.. code-block:: json

   {
       "facility_id": 1,
       "booking_date": "2025-07-15",
       "start_hour": 14,
       "end_hour": 16,
       "purpose": "Study session"
   }

Issue Management API
~~~~~~~~~~~~~~~~~~~

**Report Issue:** ``POST /report-issue``

.. code-block:: json

   {
       "title": "Broken projector in Lab A",
       "description": "The projector is not turning on...",
       "issue_type": "equipment",
       "priority": "medium",
       "location": "Lab A, Block B",
       "facility_id": 5
   }

**Update Issue Status:** ``POST /issue/<id>/update``

.. code-block:: json

   {
       "status": "in_progress",
       "admin_notes": "Technician assigned, parts ordered",
       "assigned_to": 2
   }

Database Schema Reference
------------------------

Table Relationships
~~~~~~~~~~~~~~~~~~

.. code-block:: text

   users ||--o{ issues : reports
   users ||--o{ facility_bookings : makes
   users ||--o{ issues : assigned_to
   facilities ||--o{ issues : affects
   facilities ||--o{ facility_bookings : books
   users ||--o{ chat_sessions : creates
   chat_sessions ||--o{ chat_messages : contains

Enumeration Types
~~~~~~~~~~~~~~~~

**UserRole:**

.. code-block:: python

   class UserRole(enum.Enum):
       STUDENT = "student"
       ADMIN = "admin"

**IssueStatus:**

.. code-block:: python

   class IssueStatus(enum.Enum):
       REPORTED = "reported"
       IN_PROGRESS = "in_progress" 
       RESOLVED = "resolved"
       CLOSED = "closed"

**IssueType:**

.. code-block:: python

   class IssueType(enum.Enum):
       ELECTRICAL = "electrical"
       HYGIENE = "hygiene"
       STRUCTURAL = "structural"
       EQUIPMENT = "equipment"
       SECURITY = "security"
       OTHER = "other"

**Priority:**

.. code-block:: python

   class Priority(enum.Enum):
       LOW = "low"
       MEDIUM = "medium"
       HIGH = "high"
       URGENT = "urgent"

**BookingStatus:**

.. code-block:: python

   class BookingStatus(enum.Enum):
       PENDING = "pending"
       APPROVED = "approved"
       REJECTED = "rejected"
       CANCELLED = "cancelled"

Configuration Reference
-----------------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~

.. list-table:: Environment Configuration
   :header-rows: 1
   :widths: 25 50 25

   * - Variable
     - Description
     - Required
   * - ``DATABASE_URL``
     - PostgreSQL connection string
     - Yes
   * - ``SESSION_SECRET``
     - Flask session encryption key
     - Yes
   * - ``DEEPSEEK_API_URL``
     - DeepSeek LLM API endpoint
     - No
   * - ``DEEPSEEK_MODEL``
     - Model name for LLM
     - No
   * - ``FLASK_ENV``
     - Environment (development/production)
     - No
   * - ``FLASK_DEBUG``
     - Debug mode toggle
     - No

Flask Configuration
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Application Configuration
   app.config.update(
       SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"),
       SQLALCHEMY_ENGINE_OPTIONS={
           "pool_recycle": 300,
           "pool_pre_ping": True,
       },
       SECRET_KEY=os.environ.get("SESSION_SECRET"),
       WTF_CSRF_ENABLED=True,
       WTF_CSRF_TIME_LIMIT=3600,
   )

Error Handling
-------------

HTTP Status Codes
~~~~~~~~~~~~~~~~

.. list-table:: API Response Codes
   :header-rows: 1
   :widths: 15 25 60

   * - Code
     - Status
     - Description
   * - 200
     - OK
     - Request successful
   * - 400
     - Bad Request
     - Invalid request parameters
   * - 401
     - Unauthorized
     - Authentication required
   * - 403
     - Forbidden
     - Insufficient permissions
   * - 404
     - Not Found
     - Resource not found
   * - 500
     - Internal Server Error
     - Server-side error

Error Response Format
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
       "error": {
           "code": 400,
           "message": "Validation failed",
           "details": {
               "field": "username",
               "issue": "Username already exists"
           }
       },
       "status": "error",
       "timestamp": "2025-07-03T16:45:00Z"
   }

Common Error Types
~~~~~~~~~~~~~~~~

**Authentication Errors:**

.. code-block:: python

   # Login failures
   {"error": "Invalid username or password"}
   
   # Session expired
   {"error": "Session expired, please login again"}
   
   # Insufficient permissions
   {"error": "Admin privileges required"}

**Validation Errors:**

.. code-block:: python

   # Form validation
   {"error": "Username must be 4-20 characters"}
   
   # Data integrity
   {"error": "Email address already registered"}
   
   # Business logic
   {"error": "Facility not available for booking"}

Testing and Development
----------------------

Unit Test Structure
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Test file structure
   tests/
   ├── test_models.py          # Database model tests
   ├── test_routes.py          # Route handler tests  
   ├── test_forms.py           # Form validation tests
   ├── test_ai_service.py      # AI service tests
   └── conftest.py            # Test configuration

Sample Test Cases
~~~~~~~~~~~~~~~

.. code-block:: python

   def test_user_registration():
       """Test user registration process"""
       response = client.post('/register', data={
           'username': 'testuser',
           'email': 'test@utm.edu.my', 
           'full_name': 'Test User',
           'password': 'password123',
           'password2': 'password123'
       })
       assert response.status_code == 302
       
   def test_issue_classification():
       """Test AI issue classification"""
       ai_service = AIService()
       result = ai_service.classify_issue_from_description(
           "The lights are not working in Lab A"
       )
       assert result['issue_type'] == 'electrical'

Performance Benchmarks
~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Performance Targets
   :header-rows: 1
   :widths: 40 30 30

   * - Operation
     - Target Time
     - Acceptable Range
   * - Page load (authenticated)
     - < 1 second
     - < 2 seconds
   * - Database query (simple)
     - < 50ms
     - < 100ms
   * - AI response generation
     - < 3 seconds
     - < 5 seconds
   * - User authentication
     - < 200ms
     - < 500ms
   * - Facility search
     - < 500ms
     - < 1 second