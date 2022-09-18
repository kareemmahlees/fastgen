from enum import Enum


class Database(Enum):
    sqlite3 = "sqlite3"
    postgresql = "postgresql"
    mysql = "mysql"


class PackageManager(Enum):
    pip = "pip"
    poetry = "poetry"
