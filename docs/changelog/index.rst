Changelog
=========

This document tracks all notable changes to the UTM Campus Assistant system.

Version 1.0.0 - Current Release
-------------------------------

**Release Date**: June 24, 2025

**Initial Release Features**

Core System
~~~~~~~~~~~

- Flask-based web application with SQLAlchemy ORM
- SQLite database for local development and deployment
- User authentication with bcrypt password hashing
- Role-based access control (Student/Admin)
- Responsive Bootstrap 5 dark theme UI
- UTM-branded design with university colors

User Management
~~~~~~~~~~~~~~~

- User registration and login system
- Student and administrator role support
- Profile management with student ID integration
- Secure session management
- Password reset capabilities (admin-assisted)

Facility Management
~~~~~~~~~~~~~~~~~~~

- Comprehensive facility database
- 9 different facility types with detailed specifications
- Facility search and filtering by category
- Interactive facility cards with photos
- Detailed facility descriptions and operating hours
- Campus landmarks and direction information

Issue Reporting System
~~~~~~~~~~~~~~~~~~~~~~

- Streamlined issue reporting workflow
- Issue categorization (electrical, hygiene, structural, equipment, security, other)
- Priority levels (low, medium, high, urgent)
- Status tracking (reported, in_progress, resolved, closed)
- Issue assignment to administrators
- User feedback system for resolved issues

Facility Booking System
~~~~~~~~~~~~~~~~~~~~~~~

- Online facility booking for appropriate facilities
- Booking conflict detection and prevention
- Approval workflow for booking requests
- Calendar-based booking schedule view
- Booking status management (pending, approved, rejected, cancelled)
- Admin booking management dashboard

AI-Powered Chatbot
~~~~~~~~~~~~~~~~~~

- Natural language processing for facility inquiries
- Self-hosted DeepSeek LLM integration
- Rule-based fallback system for reliability
- Context-aware responses
- Entity extraction and intent classification
- Chat history storage and retrieval

Campus Navigation
~~~~~~~~~~~~~~~~~

- Interactive campus map integration
- Step-by-step directions to facilities
- Landmark-based navigation
- Building positioning and route visualization
- Mobile-friendly direction display

Administrative Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~

- Comprehensive admin control panel
- Real-time system metrics and statistics
- User management interface
- Issue tracking and assignment
- Booking approval and management
- System monitoring and health checks

Technical Features
~~~~~~~~~~~~~~~~~~

- Gunicorn WSGI server for production deployment
- Database connection pooling and optimization
- Custom CSS with UTM brand colors and styling
- Font Awesome icons for enhanced UX
- Cross-browser compatibility
- Mobile-responsive design

Development History
-------------------

June 24, 2025
~~~~~~~~~~~~~

**Major Milestones**

- **Database Migration**: Successfully migrated from PostgreSQL to SQLite for improved portability and deployment simplicity
- **Replit Environment Migration**: Completed migration from Replit Agent to standard Replit environment
- **Booking System Enhancement**: Enhanced booking functionality with facility pre-selection from URL parameters
- **Facility Status Fix**: Fixed facility booking status - only appropriate facilities (labs, meeting rooms, event halls) are now bookable
- **Booking Button Enhancement**: Enhanced booking buttons functionality with direct facility pre-selection from facility cards

**Infrastructure Improvements**

- Added comprehensive facility data with 9 different room types and detailed specifications
- Added detailed campus directions and landmarks for all facilities based on UTM campus map
- Created dedicated directions system with interactive campus map and step-by-step routing
- Enhanced facility display with collapsible descriptions, operating hours, and landmark information
- Fixed context carrying between directions and report issue forms
- Improved campus map with accurate building positioning and interactive elements

**Visual Enhancements**

- Added custom SVG facility images with unique colors and visual branding
- Added real facility photos matching facility names, use default for missing images
- Enhanced search bar visibility by improving contrast and styling
- Added proper background colors for light theme
- Enhanced dark theme support for form controls
- Improved placeholder text readability

**Bug Fixes**

- Fixed CSRF token error in booking management
- Added admin database reset functionality
- Resolved search bar contrast issues in dark theme
- Fixed facility booking conflict detection

June 21, 2025
~~~~~~~~~~~~~

**Initial Development**

- **Project Initialization**: Initial setup with OpenAI integration
- **AI Service Migration**: Migrated from OpenAI to self-hosted DeepSeek LLM for complete local deployment
- **Reliability Enhancement**: Added fallback response system for improved reliability
- **Deployment Configuration**: Configured for ngrok deployment support
- **Environment Migration**: Successfully migrated from Replit Agent to standard Replit environment
- **Security Fixes**: Fixed CSRF token configuration and created missing view_issue.html template
- **System Redesign**: Replaced complex AI service with robust rule-based fallback system

Known Issues
------------

Current Version (1.0.0)
~~~~~~~~~~~~~~~~~~~~~~~

**Minor Issues**

- SQLAlchemy relationship warning between ChatMessage.session and ChatSession.messages (cosmetic, no functional impact)
- Mermaid diagrams not supported in Sphinx documentation (documentation build warnings)
- Some documentation cross-references show warnings during build

**Limitations**

- AI service requires manual setup and configuration
- Email notifications not yet implemented
- Advanced booking features (recurring bookings) not available
- Bulk user import requires manual script execution

**Performance Considerations**

- Large facility datasets may require pagination
- Chat history cleanup not automated
- Database size monitoring needed for high-usage environments

Planned Features
----------------

Version 1.1.0 (Planned)
~~~~~~~~~~~~~~~~~~~~~~~

**User Experience Enhancements**

- Email notification system for booking confirmations
- Password reset via email
- User profile picture uploads
- Advanced search filters for facilities

**Administrative Features**

- Bulk user import/export tools
- Advanced reporting and analytics
- System configuration UI
- Automated database maintenance

**Technical Improvements**

- Database migration system
- Automated backup scheduling
- Performance monitoring dashboard
- API endpoints for mobile app integration

Version 1.2.0 (Future)
~~~~~~~~~~~~~~~~~~~~~~

**Advanced Features**

- Mobile application support
- Multi-language support (Bahasa Malaysia)
- Integration with university LDAP/Active Directory
- Advanced booking features (recurring bookings, resource management)

**Enterprise Features**

- Role hierarchy expansion
- Department-based access control
- Advanced audit logging
- Integration with existing university systems

Breaking Changes
----------------

None in current version 1.0.0

Migration Guide
---------------

From Development to Production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Database Migration**
   
   .. code-block:: bash
   
      # Backup development database
      cp instance/utm_campus.db backups/dev_backup.db
      
      # Deploy production database
      python3 -c "from app import db; db.create_all()"

2. **Environment Configuration**
   
   Update environment variables for production:
   
   .. code-block:: bash
   
      FLASK_ENV=production
      FLASK_DEBUG=false
      SESSION_SECRET=secure-production-key

3. **Data Migration**
   
   .. code-block:: python
   
      # Migrate development data to production
      from app import app, db
      from models import User, Facility
      
      # Export and import procedures as needed

Security Updates
----------------

Current Security Measures
~~~~~~~~~~~~~~~~~~~~~~~~~

- **Authentication**: Secure user authentication with bcrypt
- **Session Management**: Secure session cookies with proper configuration
- **Input Validation**: Comprehensive form validation and CSRF protection
- **Database Security**: Parameterized queries preventing SQL injection
- **Access Control**: Role-based access with proper authorization checks

Security Recommendations
~~~~~~~~~~~~~~~~~~~~~~~~

- Regular password policy reviews
- Session timeout configuration
- Security audit logging
- Regular dependency updates
- Backup encryption implementation

Compatibility Information
-------------------------

System Requirements
~~~~~~~~~~~~~~~~~~~

**Minimum Requirements**

- Python 3.11+
- SQLite 3.31+
- Modern web browser
- 4GB RAM
- 10GB storage

**Recommended Environment**

- Ubuntu 20.04+ or similar Linux distribution
- Python 3.11+ with virtual environment
- 8GB+ RAM for production use
- SSD storage for database performance

**Browser Compatibility**

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Dependencies
~~~~~~~~~~~~

**Core Dependencies**

- Flask 2.3+
- SQLAlchemy 2.0+
- Flask-Login 0.6+
- Flask-WTF 1.1+
- Bootstrap 5.3+

**Development Dependencies**

- Sphinx 7.0+ (documentation)
- Gunicorn 21.0+ (production server)

Contributing Guidelines
-----------------------

Code Standards
~~~~~~~~~~~~~~

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Include docstrings for all functions and classes
- Maintain consistent indentation (4 spaces)

Database Changes
~~~~~~~~~~~~~~~

- Always create migration scripts for schema changes
- Test migrations on sample data before production
- Document all database changes in this changelog

Documentation Updates
~~~~~~~~~~~~~~~~~~~~~

- Update documentation for all new features
- Include code examples where appropriate
- Update this changelog for all releases

Release Process
---------------

Version Numbering
~~~~~~~~~~~~~~~~~

Using Semantic Versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in backward-compatible manner
- **PATCH**: Backward-compatible bug fixes

Release Checklist
~~~~~~~~~~~~~~~~~

1. Update version numbers in configuration
2. Update this changelog with all changes
3. Test all functionality in staging environment
4. Create database backup before deployment
5. Deploy to production environment
6. Verify all systems operational
7. Notify users of new release

Support Information
-------------------

For questions about changes or issues:

- **Technical Support**: it-support@utm.my
- **System Administrator**: admin@utm.my
- **Emergency Contact**: +60-7-553-4100

Documentation updates and feature requests can be submitted through the appropriate channels.