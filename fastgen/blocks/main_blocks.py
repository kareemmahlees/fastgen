MAIN_APP = (
    lambda project_name: f"""
            from fastapi import FastAPI

            app = FastAPI(title=f"{project_name.replace("_"," ").title()}",debug=True)

            @app.get("/")
            def root():
                return {{"msg":"Hello World"}}
"""
)

MAIN_TESTING = """
            from fastapi.testclient import TestClient
            import pytest
            from app.api.main import app

            client = TestClient(app)

            def test_main():
                res = client.get("/")
                assert res.status_code == 200
                assert res.json() == {"msg":"Hello World"}
"""
