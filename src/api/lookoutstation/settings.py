import os

JWT_SECRET = os.environ.get('JWT_SECRET', 'unsecure_fallback')

DB_HOST = os.environ.get('POSTGRES_HOSTNAME')
DB_PORT = os.environ.get('POSTGRES_PORT')
DB_USER = os.environ.get('POSTGRES_USERNAME')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_CONN = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
