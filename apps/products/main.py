import psycopg2
import os
from flask import Flask

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def get_products():
    try:
        conn = psycopg2.connect(
            host=os.getenv("PGHOST"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            database=os.getenv("PGDATABASE"),
            port=os.getenv("PGPORT")
        )
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products")
            result = cur.fetchall()
        return {"products": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(port=5002)