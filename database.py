import psycopg2
import os

try:
    c = psycopg2.connect(host=os.getenv('POSTGRES_USERNAME'), database=os.getenv('POSTGRES_DATABASE'), user=os.getenv('POSTGRES_USERNAME'), password=os.getenv('POSTGRES_PASSWORD'))
except Exception as e:
    exit(e)
