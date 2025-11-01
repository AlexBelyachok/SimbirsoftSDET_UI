import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

IS_HEADLESS = os.getenv("HEADLESS", "False").upper() == "TRUE"

if not BASE_URL:
    raise ValueError("Необходимо определить переменную BASE_URL в .env файле")