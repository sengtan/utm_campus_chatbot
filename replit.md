# UTM Campus Assistant Chatbot

## Overview

The UTM Campus Assistant Chatbot is a Flask-based web application designed to help university students and administrators manage campus facilities efficiently. The system combines a traditional web interface with an AI-powered chatbot that can understand natural language queries about facilities, handle issue reporting, and provide campus information.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with SQLAlchemy ORM
- **Database**: PostgreSQL (configured via DATABASE_URL environment variable)
- **Authentication**: Flask-Login with bcrypt password hashing
- **AI Integration**: OpenAI GPT-4o for natural language processing
- **Session Management**: Flask sessions with server-side storage

### Frontend Architecture
- **Templating**: Jinja2 templates with Bootstrap 5 dark theme
- **Styling**: Custom CSS with Font Awesome icons
- **JavaScript**: Vanilla JavaScript for chatbot interactions
- **Responsive Design**: Bootstrap grid system for mobile-first design

### Data Storage Solutions
- **Primary Database**: PostgreSQL with SQLAlchemy models
- **User Management**: Built-in Flask-Login user sessions
- **Chat History**: Stored in database with ChatSession and ChatMessage models

## Key Components

### Database Models
- **User**: Manages student and admin accounts with role-based access
- **Facility**: Stores campus facility information (labs, sports, academic buildings)
- **Issue**: Tracks facility issues with status, priority, and type classification
- **ChatSession**: Manages conversation threads between users and AI
- **ChatMessage**: Stores individual messages within chat sessions

### User Roles
- **Student**: Can report issues, chat with AI, view facilities, track their issues
- **Admin**: Full access plus issue management, user oversight, facility management

### AI Service Integration
- **Natural Language Processing**: OpenAI GPT-4o for understanding user queries
- **Entity Extraction**: Identifies facilities, issue types, and user intent
- **Context Awareness**: Maintains conversation context and facility database knowledge

### Form Validation
- **WTForms**: Comprehensive form validation for user input
- **CSRF Protection**: Built-in security for all form submissions
- **Custom Validators**: Username, email, and student ID uniqueness checks

## Data Flow

### User Registration & Authentication
1. User submits registration form with validation
2. Password hashed using bcrypt before database storage
3. Flask-Login manages session state and user authentication
4. Role-based redirects to appropriate dashboard

### Issue Reporting Flow
1. User submits issue through web form or chatbot
2. AI service classifies issue type and priority if via chatbot
3. Issue stored in database with status tracking
4. Admin receives notification and can manage issue lifecycle

### Chatbot Interaction Flow
1. User sends message via JavaScript interface
2. Message sent to Flask route handling AI processing
3. AI service extracts entities and determines intent
4. Appropriate response generated based on query type
5. Response sent back to frontend and displayed

### Facility Information System
1. Facilities loaded into AI service cache on startup
2. Users can search and filter facilities via web interface
3. AI can answer facility-related questions using cached data
4. Admin can manage facility information

## External Dependencies

### Core Dependencies
- **Flask Stack**: flask, flask-sqlalchemy, flask-login, flask-wtf, flask-bcrypt
- **Database**: psycopg2-binary for PostgreSQL connectivity
- **AI**: openai library for GPT-4o integration
- **Web Server**: gunicorn for production deployment
- **Validation**: wtforms, email-validator for form processing

### Frontend Dependencies
- **Bootstrap 5**: Dark theme variant for consistent UI
- **Font Awesome**: Icon library for enhanced UX
- **Custom CSS**: Application-specific styling

### Environment Variables Required
- **DATABASE_URL**: PostgreSQL connection string
- **SESSION_SECRET**: Flask session encryption key
- **OPENAI_API_KEY**: OpenAI API authentication

## Deployment Strategy

### Replit Configuration
- **Runtime**: Python 3.11 with Nix package management
- **Database**: PostgreSQL included in Nix configuration
- **Web Server**: Gunicorn with auto-scaling deployment target
- **Port Configuration**: Application runs on port 5000 with reload support

### Production Considerations
- **Auto-scaling**: Configured for replit autoscale deployment
- **Database Connection**: Pool recycling and pre-ping for reliability
- **Proxy Handling**: ProxyFix middleware for proper header handling
- **Security**: HTTPS termination handled by deployment platform

### Development Workflow
- **Hot Reload**: Gunicorn configured with reload for development
- **Database Migration**: SQLAlchemy handles table creation automatically
- **Environment Isolation**: Dependencies managed via pyproject.toml

## Changelog
- June 21, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.