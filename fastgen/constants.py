MAIN_APP = (
    lambda project_name: f"""
            from fastapi import FastAPI

            app = FastAPI(title=f"{project_name.replace("_"," ").title()}",debug=True)

            @app.get("/")
            def root():
                return {{"msg":"Hello World"}}
"""
)
SETTINGS = """
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
JWT_ENV_VARIABLES = """
            # ------------------- JWT Configuration -------------------------
            SECRET_KEY = 
            ALGORITHM = 
            EXPIRAY = 
"""
POSTGRES_ENV_VARIABLES = """
            # ------------------- Postgresql Configuration -------------------------
            POSTGRES_USER = 
            POSTGRES_PASSWORD = 
            POSTGRES_DB = 
            POSTGRES_HOST = 
            POSTGRES_PORT = 
"""
MYSQL_ENV_VARIABLES = """
            # ------------------- MySQL Configuration -------------------------
            MYSQL_USER = 
            MYSQL_ROOT_PASSWORD =  
            MYSQL_DATABASE = 
            MYSQL_HOST = 
            MYSQL_PORT =
        """
TESTING = """
            from fastapi.testclient import TestClient
            import pytest
            from app.api.main import app

            client = TestClient(app)
        
            def test_main():
                res = client.get("/")
                assert res.status_code == 200
                assert res.json() == {"msg":"Hello World"}
"""
DOCKERFILE = """
        FROM python:3.9

        WORKDIR /app

        COPY requirements.txt .

        RUN python -m pip install -r requirements.txt 

        EXPOSE 8000

        COPY . /app/

        CMD ["uvicorn","app.api.main:app","--host","0","--port","8000"]
"""

DOCKER_COMPOSE_BASE = (
    lambda database: f"""
        services:
            api:
                build: .
                ports:
                    - 8000:8000
                depends_on:
                    - {database}
                env_file:
                    - ./.env
"""
)
POSTGRES_DOCKER_COMPOSE = """
            postgres:
                image: postgres
                ports:
                    - 5432:5432
                env_file:
                    - ./.env
                volumes:
                - postgres-db:/var/lib/postgresql/data

        volumes:
            postgres-db:
"""
MYSQL_DOCKER_COMPOSE = """
            mysql:
                image: mysql
                ports:
                    - 3306:3306
                env_file:
                    - ./.env
                volumes:
                - mysql-db:/var/lib/mysql/data

        volumes:
            mysql-db:
"""
