# Initialize Django

1. 가상환경 셋팅
    - python3 -m venv .venv
    - source .venv/bin/activate

2. pip 최신 버전 유지
    - pip install --upgrade pip 

3. 필요한 패키지 설치
    - pip install django, djangorestframework, python-dotenv, mysqlclient, pre-commit, black

4. 장고 초기 셋팅
    - django-admin startproject config .
        - 기본 설정값들은 루트 디렉토리 안의 config에서 관리하기
    - python manage.py startapp app
        - 기본적 기능들은 이 아래에서 관리하기
    - python manage.py startapp core
        - 프로젝트에서 전반적으로 쓰이는 것들은 아래 디렉토리에서 관리
    - core/constants.py를 둬서 전역으로 쓰이는 것들을 관리
        
        ```python
        # System
        import os
        from dotenv import load_dotenv

        load_dotenv()


        class SERVICE:
            """
            Service Config
            """

            SECRET_KEY = os.getenv("SECRET_KEY")
            DEBUG = bool(os.getenv("DEBUG", False))


        class DATABASE:
            """
            Database Config
            """

            DB_NAME = os.getenv("DB_NAME")
            DB_USER = os.getenv("DB_USER")
            DB_PASSWORD = os.getenv("DB_PASSWORD")
            DB_HOST = os.getenv("DB_HOST")
            DB_PORT = os.getenv("DB_PORT")
        ```

    - .pre-commit-config.yaml 파일에서 기본 셋팅
        ```yaml
        repos:
            - repo: local
                hooks:
                - id: black
                    name: black-test
                    entry: black --check -l 150 -t py310 .
                    always_run: true
                    pass_filenames: false
                    language: system
                    types: [python]

            - repo: local
                hooks:
                - id: django-test
                    name: django-test
                    entry: python manage.py test app --keepdb --verbosity=2 --settings=config.test_settings
                    always_run: true
                    pass_filenames: false
                    language: system
                    types: [python]
        ```

    - config/test_settings.py로 테스트 셋팅 (Test DB를 생성하지 않고도 테스트)
        ```python
        from config.settings import *

        TEST_RUNNER = "config.test_runner.TestRunner"
        ```
    
    - config/test_runner.py로 테스트 셋팅
        ```python
        from django.test.runner import DiscoverRunner

        class TestRunner(DiscoverRunner):
            def setup_databases(self, **kwargs):
                """Creates the test databases by calling setup_databases()."""
                pass

            def teardown_databases(self, old_config, **kwargs):
                """Destroys the test databases, restoring pre-test conditions by calling teardown_databases()."""
                pass
        ```

    - config/settings.py DB 셋팅
        ```python
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": DATABASE.DB_NAME,
                "USER": DATABASE.DB_USER,
                "PASSWORD": DATABASE.DB_PASSWORD,
                "HOST": DATABASE.DB_HOST,
                "PORT": DATABASE.DB_PORT,
                "TEST": {
                    "NAME": DATABASE.DB_NAME,
                },
                "OPTIONS": {
                    "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                    "charset": "utf8mb4",
                    "use_unicode": True,
                },
            }
        }
        ```

5. docker로 mysql관리하기
    - 레거시는 mysql 8 version이 많으므로 해당 이미지를 받기
        - `docker pull mysql:8`

    - mysql container 실행
        - `docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=<password> -d -p 3306:3306 mysql:8`

    - mysql 설정
        - `CREATE DATABASE hello_django DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`