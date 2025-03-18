import logging
import psycopg2
import urllib

from arcade.sdk import ToolContext

# Configure the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_database_connection(context: ToolContext):
    conn_string = context.get_secret("database_url")
    logger.info(conn_string)
    p = urllib.parse.urlparse(conn_string)
    try:
        conn = psycopg2.connect(
            dbname=p.path[1:],
            user=p.username,
            password=p.password,
            host=p.hostname,
            port=p.port,
        )
        logger.info("Database connection established.")
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise e
