from dotenv import load_dotenv
load_dotenv()
from app.app import create_app
def run():
    return create_app()
