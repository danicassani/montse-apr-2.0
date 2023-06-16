import psycopg2 as pg
import dotenv, os
class PgDB:
    def __init__(self):
        dotenv.load_dotenv()
        user = os.getenv('PG_USER')
        password = os.getenv('PG_PASSWORD')
        hostname = os.getenv('PG_HOSTNAME')
        port = os.getenv('PG_PORT')
        db_name = os.getenv('PG_DB_NAME')
        DATABASE_URL=f"postgres://{user}:{password}@{hostname}:{port}/{db_name}"
        
        self.connection = pg.connect(DATABASE_URL)
        self.cursor = self.connection.cursor()
    
    #####