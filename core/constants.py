"""
    Copyright ⓒ 2023 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Project Constants
"""

# System
import os
import ast
from dotenv import load_dotenv

load_dotenv()


class SERVICE:
    # Service Config
    DEBUG = bool(os.environ.get("DEBUG", False))
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DATABASE:
    # Database Config
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")


class SYSTEM_CODE:
    # 0 ~ 999 : DEFAUT SYSTEM CODE
    SUCCESS = (0, "SUCCESS")
    CLIENT_ERROR = (1, "CLIENT_ERROR")
    UNKNOWN_SERVER_ERROR = (2, "UNKNOWN_SERVER_ERROR")
    INVALID_FORMAT = (3, "INVALID_FORMAT")
    OBJECT_DOES_NOT_EXIST = (4, "OBJECT_DOES_NOT_EXIST")
