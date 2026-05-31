from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpassword")
DB_NAME = os.getenv("DB_NAME", "assignment3_db")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def init_db():
    retries = 10
    while retries > 0:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
            print("Database initialized successfully")
            return
        except Exception as e:
            print("Waiting for database...", e)
            retries -= 1
            time.sleep(5)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "flask-api", "version": "v2"}), 200


@app.route("/api/items", methods=["GET"])
def get_items():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items), 200


@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, description) VALUES (%s, %s)",
        (name, description)
    )
    conn.commit()
    item_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Item added successfully",
        "id": item_id,
        "name": name,
        "description": description
    }), 201


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Item deleted successfully"}), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
