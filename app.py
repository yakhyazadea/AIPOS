from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Create a MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="aylin",
    password="Aylin2003",
    database="database_1"
)

def generate_unique_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"query_result_{timestamp}.html"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def execute_query():
    cursor = db.cursor()
    sql_query = request.form['query']

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()

        # Generate HTML from the query result
        html_content = "<html><head><title>Query Result</title></head><body><table border='1'>"

        # Add table headers
        html_content += "<tr>"
        for column_description in cursor.description:
            html_content += f"<th>{column_description[0]}</th>"
        html_content += "</tr>"

        # Add table rows
        for row in results:
            html_content += "<tr>"
            for value in row:
                html_content += f"<td>{value}</td>"
            html_content += "</tr>"

        html_content += "</table></body></html>"

        # Generate a unique filename
        filename = generate_unique_filename()

        # Write the HTML content to the unique file
        with open(filename, 'w') as f:
            f.write(html_content)

        # Redirect back to the query input page
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error executing SQL query: {str(e)}"
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(port=os.getenv("PORT", 5000))