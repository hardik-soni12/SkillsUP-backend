from app import create_app
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

env = os.getenv("FLASK_ENV", 'development')
print(env)

app = create_app(env)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)