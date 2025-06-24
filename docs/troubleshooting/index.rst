Troubleshooting Guide
====================

This guide helps resolve common issues with the UTM Campus Assistant system.

Common Issues
-------------

Application Won't Start
~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Application fails to start or crashes immediately

**Possible Causes and Solutions**:

1. **Missing Environment Variables**
   
   .. code-block:: bash
   
      # Check if required variables are set
      echo $SESSION_SECRET
      echo $DATABASE_URL
   
   **Solution**: Set all required environment variables

2. **Port Already in Use**
   
   .. code-block:: bash
   
      # Find process using port 5000
      lsof -i :5000
      # Kill the process or use different port
      kill -9 <PID>
   
   **Solution**: Use a different port or stop conflicting service

3. **Database Connection Issues**
   
   .. code-block:: bash
   
      # Test database connectivity
      python3 -c "from app import db; print(db.engine.url)"
   
   **Solution**: Verify database URL and credentials

Cannot Access Admin Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Users cannot access administrative features

**Diagnostic Steps**:

1. **Check User Role**
   
   .. code-block:: bash
   
      python3 -c "
      from app import app, db
      from models import User
      with app.app_context():
          user = User.query.filter_by(username='your-username').first()
          print(f'User role: {user.role}')
      "

2. **Promote User to Admin**
   
   .. code-block:: bash
   
      python3 -c "
      from app import app, db
      from models import User, UserRole
      with app.app_context():
          user = User.query.filter_by(username='your-username').first()
          user.role = UserRole.ADMIN
          db.session.commit()
      "

Chatbot Not Responding
~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: AI chatbot returns errors or no responses

**Diagnostic Steps**:

1. **Check AI Service Status**
   
   .. code-block:: bash
   
      # Test DeepSeek API
      curl -X POST http://localhost:11434/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{"model":"deepseek-r1:7b","messages":[{"role":"user","content":"test"}]}'

2. **Restart AI Service**
   
   .. code-block:: bash
   
      # For Ollama
      ollama serve
      
      # Check if model is available
      ollama list

3. **Check AI Service Logs**
   
   Review application logs for AI-related errors

Database Issues
~~~~~~~~~~~~~~~

**Symptom**: Database errors or data corruption

**Diagnostic Steps**:

1. **Check Database File Permissions**
   
   .. code-block:: bash
   
      ls -la instance/utm_campus.db
      # Ensure proper read/write permissions

2. **Test Database Connection**
   
   .. code-block:: bash
   
      python3 -c "
      from app import app, db
      with app.app_context():
          try:
              db.engine.connect()
              print('Database connection successful')
          except Exception as e:
              print(f'Database error: {e}')
      "

3. **Backup and Recreate Database**
   
   .. code-block:: bash
   
      # Backup existing database
      cp instance/utm_campus.db instance/utm_campus_backup.db
      
      # Recreate database
      python3 -c "
      from app import app, db
      with app.app_context():
          db.drop_all()
          db.create_all()
      "

Performance Issues
------------------

Slow Response Times
~~~~~~~~~~~~~~~~~~~

**Diagnostic Steps**:

1. **Check System Resources**
   
   .. code-block:: bash
   
      # Monitor CPU and memory usage
      top -p $(pgrep -f gunicorn)
      
      # Check disk usage
      df -h
      
      # Monitor network
      netstat -tuln | grep :5000

2. **Database Performance**
   
   .. code-block:: bash
   
      # Check database size
      du -h instance/utm_campus.db
      
      # Monitor database queries (if using PostgreSQL)
      # SELECT query, calls, total_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;

3. **Application Profiling**
   
   Enable debug mode temporarily to identify bottlenecks:
   
   .. code-block:: python
   
      # Add to main.py for debugging
      from werkzeug.middleware.profiler import ProfilerMiddleware
      app.wsgi_app = ProfilerMiddleware(app.wsgi_app)

High Memory Usage
~~~~~~~~~~~~~~~~~

**Diagnostic Steps**:

1. **Monitor Memory Usage**
   
   .. code-block:: bash
   
      # Check memory usage by process
      ps aux | grep gunicorn | awk '{print $2, $4, $6, $11}'

2. **Optimize Database Connections**
   
   .. code-block:: python
   
      # Adjust connection pool settings
      SQLALCHEMY_ENGINE_OPTIONS = {
          'pool_size': 5,
          'pool_recycle': 300,
          'pool_pre_ping': True
      }

Error Diagnosis
---------------

Common Error Messages
~~~~~~~~~~~~~~~~~~~~~

**"No module named 'app'"**

.. code-block:: bash

   # Ensure you're in the correct directory
   pwd
   ls -la main.py
   
   # Check Python path
   python3 -c "import sys; print(sys.path)"

**"OperationalError: no such table"**

.. code-block:: bash

   # Recreate database tables
   python3 -c "
   from app import app, db
   with app.app_context():
       db.create_all()
   "

**"CSRF token missing"**

.. code-block:: bash

   # Check if CSRF is properly configured
   python3 -c "
   from app import app
   print(app.config.get('WTF_CSRF_ENABLED', 'Not set'))
   print(app.secret_key)
   "

**"Connection refused" (AI Service)**

.. code-block:: bash

   # Check if AI service is running
   curl -f http://localhost:11434/api/version || echo "AI service not accessible"
   
   # Start AI service
   ollama serve

Log Analysis
------------

Application Logs
~~~~~~~~~~~~~~~~

**Location**: Check the console output or log files

**Common Log Patterns**:

.. code-block:: text

   # Normal operation
   INFO:root:Database tables created
   INFO:root:Loaded 9 facilities into cache
   
   # Database issues
   ERROR:sqlalchemy.engine:Cannot connect to database
   
   # AI service issues
   WARNING:ai_service:DeepSeek API not available, using fallback

**Log Analysis Commands**:

.. code-block:: bash

   # Search for errors in logs
   grep -i "error" utm_campus.log
   
   # Count error occurrences
   grep -c "ERROR" utm_campus.log
   
   # Monitor live logs
   tail -f utm_campus.log

Web Server Logs
~~~~~~~~~~~~~~~

**Gunicorn Logs**:

.. code-block:: bash

   # Check gunicorn process status
   ps aux | grep gunicorn
   
   # Monitor gunicorn logs
   journalctl -u gunicorn -f

System Recovery
---------------

Emergency Procedures
~~~~~~~~~~~~~~~~~~~~

**Complete System Reset** (Development Only):

.. warning::
   This will delete all data. Only use in development environments.

.. code-block:: bash

   # Stop the application
   pkill -f gunicorn
   
   # Backup database
   cp instance/utm_campus.db instance/backup_$(date +%Y%m%d_%H%M%S).db
   
   # Reset database
   rm instance/utm_campus.db
   
   # Restart application
   python main.py

**Database Recovery**:

.. code-block:: bash

   # Restore from backup
   cp instance/backup_YYYYMMDD_HHMMSS.db instance/utm_campus.db
   
   # Verify database integrity
   python3 -c "
   from app import app, db
   from models import User, Facility
   with app.app_context():
       print(f'Users: {User.query.count()}')
       print(f'Facilities: {Facility.query.count()}')
   "

Service Restart Procedures
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Application Restart**:

.. code-block:: bash

   # Graceful restart
   pkill -TERM -f gunicorn
   sleep 5
   python main.py
   
   # Force restart
   pkill -KILL -f gunicorn
   python main.py

**AI Service Restart**:

.. code-block:: bash

   # Restart Ollama
   pkill ollama
   ollama serve &
   
   # Wait for service to start
   sleep 10
   ollama list

Monitoring and Prevention
-------------------------

Health Checks
~~~~~~~~~~~~~

Create a health check script:

.. code-block:: python

   #!/usr/bin/env python3
   import requests
   import sys
   
   def check_health():
       try:
           # Check main application
           response = requests.get('http://localhost:5000/', timeout=10)
           if response.status_code != 200:
               return False
           
           # Check AI service
           ai_response = requests.get('http://localhost:11434/api/version', timeout=5)
           if ai_response.status_code != 200:
               print("Warning: AI service not responding")
           
           return True
       except Exception as e:
           print(f"Health check failed: {e}")
           return False
   
   if __name__ == "__main__":
       if check_health():
           print("System healthy")
           sys.exit(0)
       else:
           print("System unhealthy")
           sys.exit(1)

Preventive Maintenance
~~~~~~~~~~~~~~~~~~~~~~

**Daily Tasks**:

.. code-block:: bash

   # Check disk space
   df -h | awk '$5 > 80 {print "Warning: " $0}'
   
   # Check log file sizes
   find . -name "*.log" -size +100M -ls
   
   # Verify database integrity
   python3 -c "
   from app import app, db
   with app.app_context():
       try:
           db.engine.execute('PRAGMA integrity_check')
           print('Database integrity OK')
       except Exception as e:
           print(f'Database issue: {e}')
   "

**Weekly Tasks**:

.. code-block:: bash

   # Rotate logs
   mv utm_campus.log utm_campus.log.$(date +%Y%m%d)
   
   # Clean old backups
   find backups/ -name "*.db" -mtime +30 -delete
   
   # Update system dependencies
   pip list --outdated

Getting Additional Help
-----------------------

When to Contact Support
~~~~~~~~~~~~~~~~~~~~~~~

Contact IT support when:

- System is completely inaccessible
- Data corruption is suspected
- Security incidents occur
- Performance severely degraded
- Multiple users report issues

Support Information
~~~~~~~~~~~~~~~~~~~

**Before Contacting Support, Gather**:

1. Error messages (exact text)
2. Steps to reproduce the issue
3. System logs
4. Recent changes made
5. Number of affected users

**Contact Information**:

- **Email**: it-support@utm.my
- **Phone**: +60-7-553-4100
- **Emergency**: 24/7 support hotline

**Include in Support Requests**:

- System version information
- Environment details (development/production)
- Error logs and screenshots
- Impact assessment
- Urgency level

Useful Commands Reference
-------------------------

Quick Diagnostic Commands
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Check application status
   curl -I http://localhost:5000/
   
   # Test database connection
   python3 -c "from app import db; print('DB OK' if db.engine.connect() else 'DB Error')"
   
   # Check AI service
   curl -s http://localhost:11434/api/version | jq .
   
   # Monitor resource usage
   ps aux | grep -E "(gunicorn|python|ollama)" | awk '{print $2, $3, $4, $11}'
   
   # Check port usage
   netstat -tlnp | grep :5000

Log Commands
~~~~~~~~~~~~

.. code-block:: bash

   # View recent errors
   tail -100 utm_campus.log | grep -i error
   
   # Monitor live logs
   tail -f utm_campus.log | grep -v "GET /"
   
   # Count error types
   grep -oE "ERROR:[^:]*" utm_campus.log | sort | uniq -c
   
   # Find specific user activity
   grep "user_id=123" utm_campus.log