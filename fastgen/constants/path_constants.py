from pathlib import Path

ROUTERS_DIR: Path = Path("app/api/routers")

SCHEMAS_DIR: Path = Path("app/api/schemas")

MODELS_DIR: Path = Path("app/database/models")


ROUTER_FILE_PATH = lambda file_name: ROUTERS_DIR / f"{file_name}_router.py"

SCHEMA_FILE_PATH = lambda file_name: SCHEMAS_DIR / f"{file_name}_schema.py"

MODEL_FILE_PATH = lambda file_name: MODELS_DIR / f"{file_name}_model.py"
