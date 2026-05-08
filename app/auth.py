import os
from dotenv import load_dotenv

load_dotenv()

#считывание номера и пароля из env
HH_PHONE = os.getenv("HH_PHONE")
HH_PASSWORD = os.getenv("HH_PASSWORD")
