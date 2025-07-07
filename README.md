# UTM Campus Assistant Chatbot

A Flask-based web application for campus facility management, featuring an AI-powered chatbot, issue reporting, facility booking, and admin dashboard. This project can be hosted locally or online.

You can access this UTM Campus Chatbot web-app hosted on PythonAnywhere [here](https://tansenghooi.pythonanywhere.com/). You can also access the Sphinx documentation [here](https://tansenghooi.pythonanywhere.com/docs/).

<!-- TOC -->
## Table of Contents
- [Sample Accounts](#sample-accounts)
- [Project Structure](#project-structure)
- [Project Notes](#project-notes)
- [Documentation Structure](#documentation-structure)
- [Building Documentation](#building-documentation)
- [Features Covered](#features-covered)
- [Key Highlights](#key-highlights)
- [Hosting Options](#hosting-options)
  - [Host Locally](#host-locally)
  - [Host Online (PythonAnywhere, Free Tier)](#host-online-pythonanywhere-free-tier)
- [Database Management](#database-management)
<!-- /TOC -->

---

## Sample Accounts

**Student Accounts:**
- Username: `ada_lovelace`  
  Password: `Welcome123`
- Username: `alan_turing`  
  Password: `Welcome123`

**Admin Account:**
- Username: `admin`  
  Password: `ADMINadmin`  
  _Note: Only the admin can reset the database._

---

## Project Structure

- `ai_service.py` — AI logic, intent extraction, fallback rules
- `flask_app.py` — Flask app and extension initialization
- `main.py` — App entry point
- `models.py` — SQLAlchemy ORM models
- `forms.py` — WTForms definitions
- `routes.py` — Flask routes and business logic
- `static/` — Static assets (CSS, JS, images)
- `templates/` — Jinja2 HTML templates
- `screenshots/` — Sample screenshots of the web app
- `docs/` — Sphinx-generated documentation
- `instance/` — SQLite database and instance-specific files
- `attached_assets/` — Uploaded images and files

---

## Project Notes

- **Development History:**  
  Initial work was done on Replit. Replit's limitations (e.g., hallucination loop, inability to fix complex issues) eventually halted progress and led to the author manually continuing the implementation of this web-app.
- **Database:**  
  SQLite is used for prototyping and portability. PostgreSQL is recommended for production.
- **AI Integration:**  
  Manual integration with DeepSeek via OpenRouter.ai for cost efficiency, flexibility, and local/LAN deployment support.
- **Documentation:**  
  Sphinx is used to generate the documentation in the `docs/` folder.
- **Knowledge Base:**  
  Facility and campus knowledge is included in AI prompts and fallback logic in [`ai_service.py`](ai_service.py).
- **Screenshots:**  
  See the `screenshots/` folder and Sphinx docs for sample web-app screenshots.

---

## Documentation Structure

### Sphinx Documentation (docs/)
- **index.rst**: Main documentation index
- **installation.rst**: Installation and setup guide  
- **configuration.rst**: System configuration details
- **admin_guide.rst**: Complete administrator guide
- **user_management.rst**: User account management
- **facility_management.rst**: Facility system management
- **api_reference.rst**: Technical API documentation
- **troubleshooting.rst**: Problem resolution guide

### Simple Manuals (PDF-Ready)
- **admin_manual_simple.md**: 5-page administrator quick reference manual
- **user_manual_simple.md**: 5-page student/user guide manual

## Building Documentation

To build the complete Sphinx documentation:

```bash
cd docs
python -m sphinx -b html . _build/html
```

To convert the simple manual to PDF:

```bash
pandoc admin_manual_simple.md -o admin_manual.pdf
```

## Features Covered

1. **Component Documentation**: Complete library and function reference
2. **Configuration Notes**: All environment variables and settings
3. **Usage Guidelines**: Step-by-step administrative procedures
4. **Troubleshooting**: Common issues and solutions
5. **API Reference**: Technical implementation details

## Key Highlights

- Role-based access control (Student/Admin)
- AI-powered facility assistance with DeepSeek LLM
- Complete facility booking workflow
- Issue reporting and tracking system
- Comprehensive security and compliance features

The documentation includes screenshots from the actual application interface and provides both technical reference and practical usage guides.

## Hosting Options

### Host Locally

1. **Create API Key**
   - Register at [OpenRouter](https://openrouter.ai/), generate an API key.
   - Set the API key in your `.env` file:
     ```
     DEEPSEEK_API_KEY=your-api-key-here
     ```

2. **(Optional) Expose with Ngrok**
   - Download and run the Windows installer from [ngrok Download](https://ngrok.com/download). Follow the setup instructions to add ngrok to your system PATH.
   - Start ngrok to get a public URL:
     ```
     ngrok http --url=<your ngrok url> 5000
     ```
   - Use the ngrok URL to access the app externally.

3. **Run the App**
    ```
    python main.py
    ```

4. **Access**
- Open [http://localhost:5000](http://localhost:5000) or your ngrok URL in a browser.

---

### Host Online (PythonAnywhere, Free Tier)

1. **Create API Key**
- Register at [OpenRouter](https://openrouter.ai/), generate an API key.

2. **Deploy**
- Sign up at [PythonAnywhere](https://www.pythonanywhere.com/).
- Clone this repository.
- Refer to the `.env.example` file for required environment variables and create your own `.env` file accordingly. Export the environment variables in bash console of PythonAnywhere

3. **Access**
- Use your PythonAnywhere web app link.

**Notes for PythonAnywhere:**
- Free tier may have limited resources and external API access restrictions.
- Ensure your OpenRouter API key is set and accessible in the environment.

---

## Database Management

- **Backup database:**
    ```
    sqlite3 utm_campus.db .dump > schema.sql
    ```

- **Regenerate database:**
    ```
    sqlite3 utm_campus.db < schema.sql
    ```

---

For more details, see the [docs/](docs/) folder and in-app