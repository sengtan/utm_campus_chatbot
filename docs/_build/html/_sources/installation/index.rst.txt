Installation Guide
==================

This section covers the complete installation process for the UTM Campus Assistant system.

System Requirements
-------------------

Hardware Requirements
~~~~~~~~~~~~~~~~~~~~~

**Minimum Requirements:**

- CPU: 2 cores, 2.0 GHz
- RAM: 4 GB
- Storage: 10 GB available space
- Network: Stable internet connection

**Recommended Requirements:**

- CPU: 4 cores, 2.5 GHz or higher
- RAM: 8 GB or more
- Storage: 20 GB available space (SSD preferred)
- Network: High-speed internet connection

Software Requirements
~~~~~~~~~~~~~~~~~~~~~

**Operating System:**

- Linux (Ubuntu 20.04+ recommended)
- macOS 10.15+
- Windows 10/11 with WSL2

**Required Software:**

- Python 3.11 or higher
- Node.js 18+ (for development tools)
- Git
- SQLite3
- Web browser (Chrome, Firefox, Safari, or Edge)

Installation Methods
--------------------

There are several ways to install the UTM Campus Assistant:

1. **Replit Deployment** (Recommended for quick setup)
2. **Local Development Setup**
3. **Docker Installation** (Coming soon)
4. **Cloud Deployment** (AWS, Azure, GCP)

Replit Deployment
-----------------

The fastest way to get started is using Replit:

1. **Fork the Repository**
   
   .. code-block:: bash
   
      # Navigate to the Replit project
      # Click "Fork" to create your own copy

2. **Configure Environment Variables**
   
   Set up the following environment variables in Replit:
   
   .. code-block:: bash
   
      SESSION_SECRET=your-secure-session-key
      DATABASE_URL=sqlite:///utm_campus.db
      DEEPSEEK_API_URL=http://localhost:11434/v1/chat/completions
      DEEPSEEK_MODEL=deepseek-r1:7b

3. **Install Dependencies**
   
   Dependencies are automatically installed when you run the project.

4. **Run the Application**
   
   Click the "Run" button in Replit or use:
   
   .. code-block:: bash
   
      gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app

Local Development Setup
-----------------------

For local development and testing:

1. **Clone the Repository**
   
   .. code-block:: bash
   
      git clone https://github.com/your-org/utm-campus-assistant.git
      cd utm-campus-assistant

2. **Create Virtual Environment**
   
   .. code-block:: bash
   
      python3 -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**
   
   .. code-block:: bash
   
      pip install -r requirements.txt

4. **Set Environment Variables**
   
   Create a `.env` file:
   
   .. code-block:: bash
   
      SESSION_SECRET=your-secure-session-key-here
      DATABASE_URL=sqlite:///utm_campus.db
      DEEPSEEK_API_URL=http://localhost:11434/v1/chat/completions
      DEEPSEEK_MODEL=deepseek-r1:7b

5. **Initialize Database**
   
   .. code-block:: bash
   
      python3 -c "from app import app, db; app.app_context().push(); db.create_all()"

6. **Run the Application**
   
   .. code-block:: bash
   
      python main.py

AI Service Setup (Optional)
----------------------------

For enhanced AI capabilities, set up a local DeepSeek LLM:

Using Ollama (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Install Ollama**
   
   .. code-block:: bash
   
      curl -fsSL https://ollama.ai/install.sh | sh

2. **Download DeepSeek Model**
   
   .. code-block:: bash
   
      ollama pull deepseek-r1:7b

3. **Start Ollama Service**
   
   .. code-block:: bash
   
      ollama serve

Using vLLM
~~~~~~~~~~~

1. **Install vLLM**
   
   .. code-block:: bash
   
      pip install vllm

2. **Run DeepSeek Model**
   
   .. code-block:: bash
   
      python -m vllm.entrypoints.openai.api_server \
        --model deepseek-ai/deepseek-r1-distill-qwen-7b \
        --port 8000

Post-Installation Setup
-----------------------

1. **Access the Application**
   
   Open your web browser and navigate to:
   
   - Local: http://localhost:5000
   - Replit: Use the provided URL

2. **Create Admin Account**
   
   Register the first user account and promote it to admin:
   
   .. code-block:: bash
   
      python3 -c "
      from app import app, db
      from models import User, UserRole
      with app.app_context():
          admin = User.query.filter_by(username='your-username').first()
          admin.role = UserRole.ADMIN
          db.session.commit()
      "

3. **Initialize Facility Data**
   
   Use the admin dashboard to add initial facility data or run:
   
   .. code-block:: bash
   
      python3 -c "from routes import create_sample_data; create_sample_data()"

Verification
------------

To verify the installation is successful:

1. **Check Application Status**
   
   - Access the main page
   - Register a test user account
   - Login successfully
   - Access the chatbot interface

2. **Test Core Features**
   
   - Browse facility information
   - Submit a test issue report
   - Use the chatbot interface
   - Access admin dashboard (if admin user)

3. **Check System Health**
   
   - Verify database connectivity
   - Test AI service (if configured)
   - Check log files for errors

Troubleshooting Installation
----------------------------

Common Issues
~~~~~~~~~~~~~

**Port Already in Use**

.. code-block:: bash

   # Find process using port 5000
   lsof -i :5000
   
   # Kill the process or use different port
   gunicorn --bind 0.0.0.0:5001 --reuse-port --reload main:app

**Database Connection Errors**

.. code-block:: bash

   # Check database file permissions
   ls -la instance/utm_campus.db
   
   # Recreate database if needed
   rm instance/utm_campus.db
   python3 -c "from app import app, db; app.app_context().push(); db.create_all()"

**Module Import Errors**

.. code-block:: bash

   # Reinstall dependencies
   pip install --force-reinstall -r requirements.txt

**AI Service Connection Issues**

.. code-block:: bash

   # Check if Ollama is running
   curl http://localhost:11434/api/version
   
   # Restart Ollama service
   ollama serve

Next Steps
----------

After successful installation:

1. Read the :doc:`../configuration/index` guide
2. Complete the :doc:`../first-setup/index` process
3. Review the :doc:`../admin-dashboard/index` documentation
4. Set up :doc:`../monitoring/index` and :doc:`../backup/index`

.. note::
   Keep your installation secure by regularly updating dependencies and following the security guidelines in :doc:`../security/index`.