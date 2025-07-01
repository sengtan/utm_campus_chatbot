# UTM Campus Assistant Chatbot

A Flask-based web application for campus facility management, featuring an AI-powered chatbot, issue reporting, facility booking, and admin dashboard. This project can be hosted locally or online.

---

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