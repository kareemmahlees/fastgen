JWT_SETTINGS = """
    secret_key: str
    algorithm: str
    expiray:int
"""

POSTGRES_SETTINGS = """
    postgres_user: str
    postgres_password: str  #! needed for docker
    postgres_db: str
    postgres_host: str
    postgres_port: int
"""
MYSQL_SETTINGS = """
            mysql_user: str
            mysql_root_password: str  #! needed for docker
            mysql_database: str
            mysql_host: str
            mysql_port: int
"""
PYDANTIC_MAIN_SETTINGS = (
    lambda settings: f"""
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    {settings}

settings = Settings()
"""
)
