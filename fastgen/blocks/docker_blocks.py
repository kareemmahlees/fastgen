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
