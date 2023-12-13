from flask import Flask, request, jsonify
import mysql.connector
import logging
from logging.handlers import RotatingFileHandler

app_api = Flask(__name__)

# Configure access logging to a file
access_handler = RotatingFileHandler('access.log', maxBytes=10000, backupCount=1)
access_handler.setLevel(logging.INFO)
app_api.logger.addHandler(access_handler)

# Create a MySQL connection (you might need to update this based on your database configuration)
db = mysql.connector.connect(
    host="localhost",
    user="aylin",
    password="Aylin2003",
    database="database_1"
)

cursor = db.cursor()

@app_api.route('/execute_query', methods=['POST'])
def execute_query():
    try:
        data = request.get_json()
        sql_query = data['query']

        # Log the access
        app_api.logger.info(f"Access: {request.method} {request.url}")

        cursor.execute(sql_query)

        if "SELECT" in sql_query.upper():
            results = cursor.fetchall()

            # Convert the results to a list of dictionaries for JSON response
            result_dicts = [dict(zip(cursor.column_names, row)) for row in results]
            return jsonify({'success': True, 'results': result_dicts})
        elif "DATABASE" in sql_query.upper():
            # For non-SELECT queries, just return success
            db.commit()
            cursor.execute("SHOW DATABASES;")
            results = cursor.fetchall()
            result_dicts = [dict(zip(cursor.column_names, row)) for row in results]
            return jsonify({'success': True, 'results': result_dicts})
        elif "TABLE" in sql_query.upper():
            # For non-SELECT queries, just return success
            db.commit()
            cursor.execute("SHOW TABLES;")
            results = cursor.fetchall()
            result_dicts = [dict(zip(cursor.column_names, row)) for row in results]
            return jsonify({'success': True, 'results': result_dicts})
        else:
            # For non-SELECT queries, just return success
            db.commit()
            cursor.execute("SELECT * FROM database_1.subject;")
            results = cursor.fetchall()
            result_dicts = [dict(zip(cursor.column_names, row)) for row in results]
            return jsonify({'success': True, 'results': result_dicts})

    except Exception as e:
        app_api.logger.error(f"Error executing query: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app_api.run(port=5001)
