import os

class Config:
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    MAX_THREADS = int(os.environ.get('MAX_THREADS', '5'))
    TIMEOUT = int(os.environ.get('TIMEOUT', '30'))
    API_BASE_URL = os.environ.get('API_BASE_URL', 'https://api.example.com')
    
    @staticmethod
    def get_api_key():
        return os.environ.get('API_KEY', 'default_api_key')

