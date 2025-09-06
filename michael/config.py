import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", False)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DB_URL = os.getenv("DATABASE_URL", "sqlite:///michael.db")
