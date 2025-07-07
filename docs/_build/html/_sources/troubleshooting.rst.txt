Troubleshooting Guide
====================

This comprehensive troubleshooting guide helps administrators diagnose and resolve common issues in the UTM Campus Assistant Chatbot system.

System Startup Issues
---------------------

Application Won't Start
~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Application fails to launch or crashes immediately

**Common Causes and Solutions**:

1. **Database Connection Failed**:
   
   .. code-block:: bash
      
      # Error: could not connect to server
      # Check database status
      pg_isready -h localhost -p 5432
      
      # Verify DATABASE_URL format
      echo $DATABASE_URL
      # Should be: postgresql://user:pass@host:port/database
      
      # Test connection manually
      psql $DATABASE_URL

2. **Missing Environment Variables**:
   
   .. code-block:: bash
      
      # Check required variables
      echo $SESSION_SECRET
      echo $DATABASE_URL
      
      # Set missing variables
      export SESSION_SECRET="your-secret-key-here"
      export DATABASE_URL="postgresql://..."

3. **Port Already in Use**:
   
   .. code-block:: bash
      
      # Check what's using port 5000
      lsof -i :5000
      
      # Kill existing process
      pkill -f gunicorn
      
      # Or use different port
      gunicorn --bind 0.0.0.0:5001 main:app

4. **Python Dependencies Missing**:
   
   .. code-block:: bash
      
      # Reinstall dependencies
      pip install -r requirements.txt
      
      # Check for conflicts
      pip check

Database Issues
--------------

Table Creation Errors
~~~~~~~~~~~~~~~~~~~~

**Symptom**: Tables not created or migration errors

**Solution Steps**:

1. **Manual Table Creation**:
   
   .. code-block:: python
      
      from flask_app import app, db
      with app.app_context():
          db.drop_all()  # Caution: deletes all data
          db.create_all()

2. **Check Database Permissions**:
   
   .. code-block:: sql
      
      -- Connect as database admin
      psql -U postgres
      
      -- Grant permissions
      GRANT ALL PRIVILEGES ON DATABASE utm_campus_assistant TO your_user;
      GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;

3. **Schema Validation**:
   
   .. code-block:: bash
      
      # Check if tables exist
      psql $DATABASE_URL -c "\dt"
      
      # Verify table structure
      psql $DATABASE_URL -c "\d users"

Data Corruption Issues
~~~~~~~~~~~~~~~~~~~~

**Symptom**: Invalid data or foreign key constraint errors

**Recovery Steps**:

1. **Data Integrity Check**:
   
   .. code-block:: sql
      
      -- Check for orphaned records
      SELECT * FROM issues WHERE user_id NOT IN (SELECT id FROM users);
      SELECT * FROM facility_bookings WHERE facility_id NOT IN (SELECT id FROM facilities);

2. **Clean Up Orphaned Data**:
   
   .. code-block:: sql
      
      -- Remove orphaned issues
      DELETE FROM issues WHERE user_id NOT IN (SELECT id FROM users);
      
      -- Remove orphaned bookings  
      DELETE FROM facility_bookings WHERE facility_id NOT IN (SELECT id FROM facilities);

3. **Reset to Clean State**:
   
   Use the admin interface database reset function or:
   
   .. code-block:: python
      
      # Access /admin/reset-database endpoint as admin
      # This will recreate all tables with sample data

Authentication Problems
----------------------

User Cannot Login
~~~~~~~~~~~~~~~~

**Symptom**: Valid credentials rejected

**Diagnostic Steps**:

1. **Check User Account Status**:
   
   .. code-block:: sql
      
      SELECT username, email, created_at FROM users WHERE username = 'problem_user';

2. **Password Hash Verification**:
   
   .. code-block:: python
      
      from flask_bcrypt import Bcrypt
      bcrypt = Bcrypt()
      
      # Test password hashing
      test_hash = bcrypt.generate_password_hash('test_password')
      print(bcrypt.check_password_hash(test_hash, 'test_password'))

3. **Session Configuration**:
   
   .. code-block:: bash
      
      # Verify session secret is set
      echo $SESSION_SECRET
      
      # Check for session conflicts
      # Clear browser cookies and try again

Session Timeouts
~~~~~~~~~~~~~~~

**Symptom**: Users logged out unexpectedly

**Solutions**:

1. **Extend Session Timeout**:
   
   .. code-block:: python
      
      # In flask_app.py, adjust session configuration
      from datetime import timedelta
      app.permanent_session_lifetime = timedelta(hours=24)

2. **Check Session Storage**:
   
   .. code-block:: bash
      
      # Ensure sufficient disk space for session files
      df -h /tmp

3. **Session Cookie Issues**:
   
   Check browser console for cookie-related errors and ensure HTTPS is properly configured.

AI Service Issues
----------------

DeepSeek LLM Not Responding
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Chatbot returns fallback responses or errors

**Diagnostic Steps**:

1. **Check LLM Service Status**:
   
   .. code-block:: bash
      
      # Test API endpoint
      curl http://localhost:11434/v1/models
      
      # Check if Ollama is running
      ps aux | grep ollama

2. **Verify API Configuration**:
   
   .. code-block:: bash
      
      echo $DEEPSEEK_API_URL
      echo $DEEPSEEK_MODEL
      
      # Test manual API call
      curl -X POST http://localhost:11434/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{"model":"deepseek-r1:7b","messages":[{"role":"user","content":"Hello"}]}'

3. **Restart LLM Service**:
   
   .. code-block:: bash
      
      # For Ollama
      pkill ollama
      ollama serve &
      
      # For vLLM
      pkill -f vllm
      python -m vllm.entrypoints.openai.api_server --model deepseek-ai/deepseek-r1-distill-qwen-7b --port 8000 &

Slow AI Response Times
~~~~~~~~~~~~~~~~~~~~

**Symptom**: Chatbot takes too long to respond

**Optimization Steps**:

1. **Check System Resources**:
   
   .. code-block:: bash
      
      # Monitor CPU and memory usage
      htop
      
      # Check GPU usage (if applicable)
      nvidia-smi

2. **Adjust Timeout Settings**:
   
   .. code-block:: python
      
      # In ai_service.py
      class AIService:
          timeout = 30  # Reduce from 60 seconds

3. **Model Optimization**:
   
   .. code-block:: bash
      
      # Use smaller model for faster responses
      export DEEPSEEK_MODEL="deepseek-r1:1.5b"
      
      # Or increase hardware resources

Chatbot Response Quality Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Inappropriate or inaccurate responses

**Solutions**:

1. **Update Facility Cache**:
   
   .. code-block:: python
      
      # Refresh facility information
      # Access /admin/refresh-cache endpoint

2. **Review System Prompts**:
   
   Check and update the system prompts in `ai_service.py` to improve response quality.

3. **Fallback System Check**:
   
   Ensure fallback responses are appropriate when AI service is unavailable.

Frontend Issues
--------------

Chatbot Interface Not Loading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Chat interface doesn't appear or respond

**Solutions**:

1. **Check JavaScript Console**:
   
   .. code-block:: javascript
      
      // Open browser console (F12) and look for errors
      // Common errors:
      // - Failed to fetch
      // - CSRF token missing
      // - Network connectivity issues

2. **Verify Static Files**:
   
   .. code-block:: bash
      
      # Check if JavaScript files exist
      ls -la static/js/chatbot.js
      
      # Verify file permissions
      chmod 644 static/js/chatbot.js

3. **CSRF Token Issues**:
   
   .. code-block:: html
      
      <!-- Ensure CSRF token is present in templates -->
      <meta name="csrf-token" content="{{ csrf_token() }}">

Form Submission Errors
~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Forms don't submit or show validation errors

**Diagnostic Steps**:

1. **Check Form Configuration**:
   
   .. code-block:: python
      
      # Verify CSRF is enabled
      app.config['WTF_CSRF_ENABLED'] = True
      
      # Check form validation in forms.py

2. **Validation Error Debugging**:
   
   .. code-block:: python
      
      # Add debugging to form handlers
      if form.validate_on_submit():
          # Form is valid
          pass
      else:
          print(form.errors)  # Debug validation errors

Performance Issues
-----------------

Slow Page Load Times
~~~~~~~~~~~~~~~~~~

**Symptom**: Pages take too long to load

**Optimization Steps**:

1. **Database Query Optimization**:
   
   .. code-block:: python
      
      # Enable SQL query logging
      app.config['SQLALCHEMY_ECHO'] = True
      
      # Look for N+1 query problems
      # Use eager loading for relationships

2. **Static File Optimization**:
   
   .. code-block:: bash
      
      # Compress CSS and JavaScript files
      # Enable gzip compression in web server
      # Use CDN for Bootstrap and other libraries

3. **Database Connection Pooling**:
   
   .. code-block:: python
      
      # Adjust connection pool settings
      app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
          "pool_recycle": 300,
          "pool_pre_ping": True,
          "pool_size": 10,
          "max_overflow": 20,
      }

High Memory Usage
~~~~~~~~~~~~~~~

**Symptom**: Application consuming too much memory

**Solutions**:

1. **Monitor Memory Usage**:
   
   .. code-block:: bash
      
      # Check memory consumption
      ps aux | grep gunicorn
      
      # Monitor over time
      top -p $(pgrep gunicorn)

2. **Optimize Database Queries**:
   
   .. code-block:: python
      
      # Use pagination for large result sets
      issues = Issue.query.paginate(page=1, per_page=20)
      
      # Close database sessions properly
      db.session.close()

3. **Configure Gunicorn Workers**:
   
   .. code-block:: bash
      
      # Adjust worker count based on available memory
      gunicorn --workers 2 --bind 0.0.0.0:5000 main:app

Booking System Issues
--------------------

Booking Conflicts
~~~~~~~~~~~~~~~~

**Symptom**: Double bookings or scheduling conflicts

**Solutions**:

1. **Database Constraint Check**:
   
   .. code-block:: sql
      
      -- Add unique constraint to prevent conflicts
      ALTER TABLE facility_bookings 
      ADD CONSTRAINT unique_booking 
      UNIQUE (facility_id, booking_date, start_hour, end_hour);

2. **Validation Logic**:
   
   .. code-block:: python
      
      # Check for existing bookings before approval
      existing = FacilityBooking.query.filter(
          FacilityBooking.facility_id == booking.facility_id,
          FacilityBooking.booking_date == booking.booking_date,
          FacilityBooking.status == BookingStatus.APPROVED
      ).all()

Booking Approval Issues
~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Bookings stuck in pending status

**Solutions**:

1. **Check Admin Notifications**:
   
   Ensure admins are receiving notifications about pending bookings.

2. **Review Approval Workflow**:
   
   .. code-block:: python
      
      # Verify admin permissions
      @admin_required
      def update_booking(booking_id):
          # Check user has admin role

3. **Automated Approval Rules**:
   
   Consider implementing automatic approval for certain booking types.

Facility Information Issues
--------------------------

Outdated Facility Data
~~~~~~~~~~~~~~~~~~~~

**Symptom**: Incorrect facility information displayed

**Solutions**:

1. **Update Facility Records**:
   
   Use admin interface to update facility information or directly update database.

2. **Cache Refresh**:
   
   .. code-block:: python
      
      # Force cache refresh in AI service
      ai_service.load_facilities()

3. **Data Validation**:
   
   .. code-block:: sql
      
      -- Check for facilities with missing information
      SELECT * FROM facilities WHERE location IS NULL OR location = '';

Directions Not Working
~~~~~~~~~~~~~~~~~~~~

**Symptom**: Facility directions not displaying properly

**Solutions**:

1. **Check Location Data**:
   
   Ensure all facilities have complete location information.

2. **Verify Direction Algorithm**:
   
   .. code-block:: python
      
      # Test direction generation
      from routes import get_facility_directions
      directions = get_facility_directions(facility)

Security Issues
--------------

Unauthorized Access
~~~~~~~~~~~~~~~~~

**Symptom**: Users accessing admin functions

**Solutions**:

1. **Check Role Decorators**:
   
   .. code-block:: python
      
      # Ensure all admin routes are protected
      @admin_required
      def admin_function():
          pass

2. **Session Security**:
   
   .. code-block:: python
      
      # Verify session configuration
      app.config.update(
          SESSION_COOKIE_SECURE=True,  # HTTPS only
          SESSION_COOKIE_HTTPONLY=True,  # No JavaScript access
          SESSION_COOKIE_SAMESITE='Lax',  # CSRF protection
      )

CSRF Token Errors
~~~~~~~~~~~~~~~

**Symptom**: CSRF validation failed errors

**Solutions**:

1. **Token Generation**:
   
   .. code-block:: html
      
      <!-- Ensure token is included in forms -->
      {{ csrf_token() }}

2. **Ajax Requests**:
   
   .. code-block:: javascript
      
      // Include CSRF token in fetch requests
      fetch('/api/endpoint', {
          headers: {
              'X-CSRFToken': document.querySelector('[name=csrf-token]').content
          }
      });

Monitoring and Logging
---------------------

Log Analysis
~~~~~~~~~~~

**Application Logs**:

.. code-block:: bash

   # Check application logs
   tail -f /var/log/utm_assistant.log
   
   # Filter for errors
   grep ERROR /var/log/utm_assistant.log
   
   # Monitor database queries
   grep "SELECT\|INSERT\|UPDATE\|DELETE" /var/log/utm_assistant.log

**Database Logs**:

.. code-block:: bash

   # PostgreSQL logs
   tail -f /var/log/postgresql/postgresql-*.log
   
   # Check for connection issues
   grep "connection" /var/log/postgresql/postgresql-*.log

System Health Checks
~~~~~~~~~~~~~~~~~~~

**Automated Monitoring Script**:

.. code-block:: bash

   #!/bin/bash
   # health_check.sh
   
   # Check application response
   curl -f http://localhost:5000/ || echo "Application down"
   
   # Check database connectivity
   pg_isready -h localhost -p 5432 || echo "Database down"
   
   # Check AI service
   curl -f http://localhost:11434/v1/models || echo "AI service down"
   
   # Check disk space
   df -h | awk '$5 > 85 {print "Disk space warning: " $0}'

Emergency Procedures
-------------------

Complete System Recovery
~~~~~~~~~~~~~~~~~~~~~~

**If system is completely down**:

1. **Check Service Status**:
   
   .. code-block:: bash
      
      systemctl status postgresql
      systemctl status nginx  # if using reverse proxy
      ps aux | grep gunicorn

2. **Restart Services**:
   
   .. code-block:: bash
      
      # Restart database
      sudo systemctl restart postgresql
      
      # Restart application
      pkill gunicorn
      gunicorn --bind 0.0.0.0:5000 main:app

3. **Restore from Backup**:
   
   .. code-block:: bash
      
      # Restore database backup
      psql utm_campus_assistant < backup_latest.sql
      
      # Verify data integrity
      psql utm_campus_assistant -c "SELECT COUNT(*) FROM users;"

Data Recovery
~~~~~~~~~~~

**If data is corrupted or lost**:

1. **Stop Application**:
   
   .. code-block:: bash
      
      pkill gunicorn

2. **Restore Database**:
   
   .. code-block:: bash
      
      dropdb utm_campus_assistant
      createdb utm_campus_assistant
      psql utm_campus_assistant < backup_YYYYMMDD.sql

3. **Verify Restoration**:
   
   .. code-block:: bash
      
      # Check table counts
      psql utm_campus_assistant -c "\dt+"
      
      # Verify user accounts
      psql utm_campus_assistant -c "SELECT COUNT(*) FROM users;"

4. **Restart Application**:
   
   .. code-block:: bash
      
      gunicorn --bind 0.0.0.0:5000 main:app

Getting Help
-----------

Support Resources
~~~~~~~~~~~~~~~

1. **Check Documentation**:
   - Review this troubleshooting guide
   - Consult API reference documentation
   - Check configuration documentation

2. **Review Logs**:
   - Application error logs
   - Database connection logs
   - System resource usage

3. **Community Support**:
   - Flask documentation and community
   - PostgreSQL support resources
   - DeepSeek/Ollama documentation

4. **Professional Support**:
   - Contact system administrator
   - Escalate to development team
   - Consider professional consultation

Escalation Procedures
~~~~~~~~~~~~~~~~~~~

**When to Escalate**:

- Security breaches or suspected attacks
- Data corruption or loss
- System performance severely degraded
- Multiple component failures
- Unable to resolve within 2 hours

**Escalation Information to Provide**:

- Description of the problem
- Steps already attempted
- Error messages and logs
- System configuration details
- Impact on users and operations