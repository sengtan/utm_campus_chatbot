Configuration Guide
===================

This guide covers all configuration options for the UTM Campus Assistant system.

Environment Variables
----------------------

Core Configuration
~~~~~~~~~~~~~~~~~~

.. list-table:: Required Environment Variables
   :widths: 30 20 50
   :header-rows: 1

   * - Variable
     - Default
     - Description
   * - SESSION_SECRET
     - None
     - Flask session encryption key (required)
   * - DATABASE_URL
     - sqlite:///utm_campus.db
     - Database connection string
   * - DEEPSEEK_API_URL
     - http://localhost:11434/v1/chat/completions
     - AI service endpoint
   * - DEEPSEEK_MODEL
     - deepseek-r1:7b
     - AI model identifier

Application Settings
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Flask Configuration
   FLASK_ENV=production
   FLASK_DEBUG=false
   
   # Database Settings
   SQLALCHEMY_TRACK_MODIFICATIONS=false
   SQLALCHEMY_ECHO=false
   
   # Security Settings
   SESSION_COOKIE_SECURE=true
   SESSION_COOKIE_HTTPONLY=true
   SESSION_COOKIE_SAMESITE=Lax

Database Configuration
----------------------

SQLite Configuration
~~~~~~~~~~~~~~~~~~~~

Default configuration for development and small deployments:

.. code-block:: python

   SQLALCHEMY_DATABASE_URI = 'sqlite:///utm_campus.db'
   SQLALCHEMY_ENGINE_OPTIONS = {
       'pool_recycle': 300,
       'pool_pre_ping': True,
   }

PostgreSQL Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

For production deployments with high load:

.. code-block:: bash

   DATABASE_URL=postgresql://username:password@localhost:5432/utm_campus

.. code-block:: python

   SQLALCHEMY_ENGINE_OPTIONS = {
       'pool_size': 10,
       'pool_recycle': 3600,
       'pool_pre_ping': True,
       'max_overflow': 20
   }

AI Service Configuration
------------------------

Local DeepSeek Setup
~~~~~~~~~~~~~~~~~~~~

Configure for local AI service:

.. code-block:: bash

   DEEPSEEK_API_URL=http://localhost:11434/v1/chat/completions
   DEEPSEEK_MODEL=deepseek-r1:7b
   DEEPSEEK_TIMEOUT=30
   DEEPSEEK_MAX_RETRIES=3

OpenAI Configuration
~~~~~~~~~~~~~~~~~~~~

Alternative AI service configuration:

.. code-block:: bash

   OPENAI_API_KEY=your-api-key-here
   OPENAI_MODEL=gpt-4
   OPENAI_MAX_TOKENS=1000

Security Configuration
----------------------

Session Security
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Session configuration
   PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
   SESSION_COOKIE_SECURE = True
   SESSION_COOKIE_HTTPONLY = True
   SESSION_COOKIE_SAMESITE = 'Lax'

Password Security
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Password hashing configuration
   BCRYPT_LOG_ROUNDS = 12
   PASSWORD_MIN_LENGTH = 8
   PASSWORD_REQUIRE_SPECIAL = True

Logging Configuration
---------------------

Application Logging
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s %(levelname)s %(name)s %(message)s',
       handlers=[
           logging.FileHandler('utm_campus.log'),
           logging.StreamHandler()
       ]
   )

Log Levels
~~~~~~~~~~

.. list-table:: Log Levels
   :widths: 20 80
   :header-rows: 1

   * - Level
     - Usage
   * - DEBUG
     - Development debugging
   * - INFO
     - General information
   * - WARNING
     - Warning messages
   * - ERROR
     - Error conditions
   * - CRITICAL
     - Critical failures

Performance Configuration
-------------------------

Cache Settings
~~~~~~~~~~~~~~

.. code-block:: python

   # Facility cache configuration
   FACILITY_CACHE_TIMEOUT = 3600  # 1 hour
   AI_RESPONSE_CACHE = True
   CACHE_TYPE = 'simple'

Database Optimization
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Query optimization
   SQLALCHEMY_ENGINE_OPTIONS = {
       'pool_size': 20,
       'pool_recycle': 3600,
       'pool_pre_ping': True,
       'echo': False,
       'echo_pool': False
   }

File Upload Configuration
-------------------------

Upload Settings
~~~~~~~~~~~~~~~

.. code-block:: python

   # File upload configuration
   MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
   UPLOAD_FOLDER = 'uploads'
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

Storage Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # File storage paths
   STATIC_FOLDER=static
   UPLOAD_FOLDER=uploads
   BACKUP_FOLDER=backups

Email Configuration
-------------------

SMTP Settings
~~~~~~~~~~~~~

.. code-block:: bash

   # Email configuration
   MAIL_SERVER=smtp.utm.my
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=utm-campus-assistant@utm.my
   MAIL_PASSWORD=your-email-password

Email Templates
~~~~~~~~~~~~~~~

Configure email notifications:

.. code-block:: python

   # Email settings
   MAIL_DEFAULT_SENDER = 'UTM Campus Assistant <noreply@utm.my>'
   MAIL_SUBJECT_PREFIX = '[UTM Campus] '

Backup Configuration
--------------------

Database Backup
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Backup settings
   BACKUP_SCHEDULE=daily
   BACKUP_RETENTION_DAYS=30
   BACKUP_LOCATION=/backups/utm_campus

Automated Backups
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Cron job for daily backups
   0 2 * * * /path/to/backup_script.sh

Monitoring Configuration
------------------------

Health Check Settings
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Health monitoring
   HEALTH_CHECK_INTERVAL = 300  # 5 minutes
   HEALTH_CHECK_ENDPOINTS = [
       '/health',
       '/api/status',
       '/db/ping'
   ]

Metrics Collection
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Metrics configuration
   METRICS_ENABLED = True
   METRICS_ENDPOINT = '/metrics'
   METRICS_RETENTION_DAYS = 90

Development Configuration
-------------------------

Debug Settings
~~~~~~~~~~~~~~

.. code-block:: bash

   # Development environment
   FLASK_ENV=development
   FLASK_DEBUG=true
   SQLALCHEMY_ECHO=true
   LOG_LEVEL=DEBUG

Testing Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Test database
   TEST_DATABASE_URL = 'sqlite:///:memory:'
   TESTING = True
   WTF_CSRF_ENABLED = False

Production Configuration
------------------------

Optimization Settings
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Production environment
   FLASK_ENV=production
   FLASK_DEBUG=false
   SQLALCHEMY_ECHO=false
   LOG_LEVEL=INFO

Security Hardening
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Production security
   SESSION_COOKIE_SECURE = True
   PREFERRED_URL_SCHEME = 'https'
   FORCE_HTTPS = True

Configuration Validation
-------------------------

Required Settings Check
~~~~~~~~~~~~~~~~~~~~~~~

Create a validation script:

.. code-block:: python

   def validate_config():
       required_vars = [
           'SESSION_SECRET',
           'DATABASE_URL'
       ]
       
       for var in required_vars:
           if not os.getenv(var):
               raise ValueError(f"Missing required environment variable: {var}")

Configuration Templates
-----------------------

Development Template
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # .env.development
   SESSION_SECRET=dev-secret-key-change-in-production
   DATABASE_URL=sqlite:///utm_campus_dev.db
   FLASK_ENV=development
   FLASK_DEBUG=true
   DEEPSEEK_API_URL=http://localhost:11434/v1/chat/completions
   DEEPSEEK_MODEL=deepseek-r1:7b

Production Template
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # .env.production
   SESSION_SECRET=secure-random-key-here
   DATABASE_URL=postgresql://user:pass@localhost/utm_campus
   FLASK_ENV=production
   FLASK_DEBUG=false
   DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
   DEEPSEEK_MODEL=deepseek-r1:7b

Best Practices
--------------

Security Best Practices
~~~~~~~~~~~~~~~~~~~~~~~

1. **Never commit secrets to version control**
2. **Use strong, unique session secrets**
3. **Enable HTTPS in production**
4. **Regularly rotate API keys**
5. **Monitor access logs**

Performance Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Use connection pooling**
2. **Enable query caching**
3. **Optimize database queries**
4. **Monitor resource usage**
5. **Use CDN for static assets**

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Use environment-specific configs**
2. **Document all configuration options**
3. **Validate configuration on startup**
4. **Use configuration management tools**
5. **Backup configuration files**