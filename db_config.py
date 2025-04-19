import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])  # Default PostgreSQL port
    



# Exported from Render on 2025-04-18T10:52:58Z
# databases:
# - name: db.ask
#   databaseName: db_ask_n9vk
#   user: db_ask_n9vk_user
#   plan: free
#   region: singapore
#   ipAllowList:
#   - source: 0.0.0.0/0
#     description: everywhere
#   postgresMajorVersion: "16"
# version: "1"

