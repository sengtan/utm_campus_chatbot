Installation and Setup
=====================

System Requirements
------------------

Hardware Requirements
~~~~~~~~~~~~~~~~~~~~~
- **Minimum**: 2GB RAM, 1 CPU core, 5GB storage
- **Recommended**: 4GB RAM, 2 CPU cores, 10GB storage
- **Operating System**: Linux (Ubuntu 18.04+), macOS 10.15+, Windows 10+

Software Dependencies
~~~~~~~~~~~~~~~~~~~~
- Python 3.11+
- PostgreSQL 12+
- Node.js 18+ (for frontend dependencies)
- Git for version control

Installation Methods
-------------------

Replit Deployment (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Import Project**:
   
   .. code-block:: bash
      
      # Clone or import the project to Replit
      # All dependencies are managed via pyproject.toml

2. **Environment Setup**:
   
   The system automatically configures:
   - Python 3.11 runtime
   - PostgreSQL database
   - Required Python packages
   - Gunicorn web server

3. **Database Configuration**:
   
   .. code-block:: bash
      
      # Database is automatically created and configured
      # Tables are created on first run

Self-Hosted Deployment
~~~~~~~~~~~~~~~~~~~~~

1. **Clone Repository**:
   
   .. code-block:: bash
      
      git clone <repository-url>
      cd utm-campus-assistant

2. **Install Dependencies**:
   
   .. code-block:: bash
      
      pip install -r requirements.txt

3. **Database Setup**:
   
   .. code-block:: bash
      
      # Create PostgreSQL database
      createdb utm_campus_assistant
      
      # Set environment variables
      export DATABASE_URL="postgresql://user:password@localhost/utm_campus_assistant"
      export SESSION_SECRET="your-secret-key"

4. **DeepSeek LLM Setup**:
   
   .. code-block:: bash
      
      # Option A: Using Ollama
      curl -fsSL https://ollama.ai/install.sh | sh
      ollama pull deepseek-r1:7b
      ollama serve
      
      # Option B: Using vLLM
      pip install vllm
      python -m vllm.entrypoints.openai.api_server \
        --model deepseek-ai/deepseek-r1-distill-qwen-7b \
        --port 8000

5. **Start Application**:
   
   .. code-block:: bash
      
      python main.py

Environment Variables
--------------------

Required Variables
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - Variable
     - Description
     - Default Value
   * - ``DATABASE_URL``
     - PostgreSQL connection string
     - Auto-configured on Replit
   * - ``SESSION_SECRET``
     - Flask session encryption key
     - Auto-generated on Replit
   * - ``DEEPSEEK_API_URL``
     - DeepSeek LLM API endpoint
     - ``http://localhost:11434/v1/chat/completions``
   * - ``DEEPSEEK_MODEL``
     - DeepSeek model name
     - ``deepseek-r1:7b``

Optional Variables
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - Variable
     - Description
     - Default Value
   * - ``FLASK_ENV``
     - Application environment
     - ``production``
   * - ``FLASK_DEBUG``
     - Debug mode toggle
     - ``False``

Initial Configuration
--------------------

Database Initialization
~~~~~~~~~~~~~~~~~~~~~~

1. **Automatic Setup**: On first run, the application automatically:
   
   - Creates all database tables
   - Loads sample facility data
   - Sets up administrative user structure

2. **Manual Setup** (if needed):
   
   .. code-block:: python
      
      from flask_app import app, db
      with app.app_context():
          db.create_all()

Admin User Creation
~~~~~~~~~~~~~~~~~~

1. Navigate to the registration page
2. Create an admin account:
   
   - Username: ``admin``
   - Email: ``admin@utm.edu.my``
   - Role: ``Admin``
   - Password: Set a secure password

Sample Data Loading
~~~~~~~~~~~~~~~~~~

The system includes sample facilities for testing:

- Academic buildings
- Laboratories
- Sports facilities
- Administrative offices
- Dining halls

Verification Steps
-----------------

1. **Application Start**:
   
   .. code-block:: bash
      
      # Check application logs
      [INFO] Starting gunicorn
      [INFO] Database tables created
      [INFO] Loaded X facilities into cache

2. **Database Connection**:
   
   .. code-block:: bash
      
      # Verify database connectivity
      # Check facility count in logs

3. **Web Interface**:
   
   - Navigate to application URL
   - Verify login page loads
   - Test user registration
   - Check admin dashboard access

Troubleshooting Installation
---------------------------

Common Issues
~~~~~~~~~~~~

**Database Connection Failed**:

.. code-block:: bash
   
   # Check DATABASE_URL format
   export DATABASE_URL="postgresql://username:password@host:port/database"

**DeepSeek LLM Not Responding**:

.. code-block:: bash
   
   # Verify LLM service is running
   curl http://localhost:11434/v1/models
   
   # Check API URL configuration
   export DEEPSEEK_API_URL="http://localhost:11434/v1/chat/completions"

**Port Already in Use**:

.. code-block:: bash
   
   # Kill existing processes
   pkill -f gunicorn
   
   # Or use different port
   gunicorn --bind 0.0.0.0:5001 main:app

**Permission Errors**:

.. code-block:: bash
   
   # Check file permissions
   chmod +x main.py
   
   # Ensure write access to instance directory
   mkdir -p instance
   chmod 755 instance