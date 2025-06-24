from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask_app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)