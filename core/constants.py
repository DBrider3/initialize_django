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
    ACCESS_TOKEN_EXP_MIN = int(os.environ.get("ACCESS_TOKEN_EXP_MIN"))  # ACCESS TOKEN EXPIRE MININUTE
    REFRESH_TOKEN_EXP_DAY = int(os.environ.get("REFRESH_TOKEN_EXP_DAY"))  # REFRESH TOKEN EXPIRE DAYS


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

    # 1000 ~ 1999 : AUTH SYSTEM CODE
    AUTH_REQUIRED = (1000, "AUTH_REQUIRED")
    TOKEN_EXPIRED = (1001, "TOKEN_EXPIRED")
    TOKEN_INVALID = (1002, "TOKEN_INVALID")

    # 2000 ~ 2999 : USER SYSTEM CODE
    USER_NOT_FOUND = (2000, "USER_NOT_FOUND")
    USER_ALREADY_EXIST = (2001, "USER_ALREADY_EXIST")
    USER_NOT_ACTIVE = (2002, "USER_NOT_ACTIVE")
    USER_INVALID_PASSWORD = (2003, "USER_INVALID_PASSWORD")
    USER_USERNAME_EXIST = (2004, "USER_USERNAME_EXIST")

    # 3000 ~ 3999 : ARTICLE SYSTEM CODE
    ARTICLE_NOT_FOUND = (3000, "ARTICLE_NOT_FOUND")
    ARTICLE_CREATE_ERROR = (3001, "ARTICLE_CREATE_ERROR")
    COMMENT_NOT_FOUND = (3002, "COMMENT_NOT_FOUND")
