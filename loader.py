from connect import connection 
from elasticsearch import Elasticsearch
import logging
import mysql.connector

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to Elasticsearch
es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

index_name = "jobs_listing"

# Create the index if it does not exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)
    logger.info(f"Index '{index_name}' created.")
else:
    logger.info(f"Index '{index_name}' already exists.")

# Connect to MySQL database

mysql_con = connection()
mysql_cur = mysql_con.cursor()

try:
    # Query to select unique titles from the job_postings table
    select_query = "SELECT DISTINCT position FROM jobs_listing"
    mysql_cur.execute(select_query)
    records = mysql_cur.fetchall()
    
    # Index each unique title into Elasticsearch
    for i, line in enumerate(records):
        document = {
            "position": line[0],  # Change to line[0] to access the position correctly
        }
        if document["position"]:
            es.index(index=index_name, document=document)
            logger.info(f"Indexed document {i + 1}: {document}")

except mysql.connector.Error as e:
    logger.error(f"MySQL error: {e}")
except Exception as e:
    logger.error(f"Error: {e}")
finally:
    # Ensure resources are closed
    if mysql_cur:
        mysql_cur.close()
    if mysql_con:
        mysql_con.close()