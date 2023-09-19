from .config import DATABASE_PARAMETERS
import psycopg2

# Create our connection pool
connection = psycopg2.connect(**DATABASE_PARAMETERS)
