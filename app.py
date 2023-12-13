from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
import requests
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure access logging to a file
access_handler = RotatingFileHandler('access.log', maxBytes=10000, backupCount=1)
access_handler.setLevel(logging.INFO)
app.logger.addHandler(access_handler)

def generate_unique_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"query_result_{timestamp}.html"

@app.route('/')
def index():
    app.logger.info(f"Access: {request.method} {request.url}")
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def execute_query():
    sql_query = request.form['query']
    api_url = 'http://localhost:5001/execute_query'

    try:
        response = requests.post(api_url, json={'query': sql_query})
        response_data = response.json()

        if response_data['success']:
            results = response_data['results']

            # Generate HTML from the query result
            html_content = "<html><head><title>Query Result</title></head><body><table border='1'>"

            # Add table headers
            html_content += "<tr>"
            for column_name in results[0]:
                html_content += f"<th>{column_name}</th>"
            html_content += "</tr>"

            # Add table rows
            for row in results:
                html_content += "<tr>"
                for value in row.values():
                    html_content += f"<td>{value}</td>"
                html_content += "</tr>"

            html_content += "</table></body></html>"

            # Generate a unique filename
            filename = generate_unique_filename()

            # Write the HTML content to the unique file
            with open(filename, 'w') as f:
                f.write(html_content)

            # Log the access
            app.logger.info(f"Access: {request.method} {request.url}")

            # Redirect back to the query input page
            return redirect(url_for('index'))
        else:
            app.logger.error(f"Error executing SQL query: {response_data['error']}")
            return f"Error executing SQL query: {response_data['error']}"
    except Exception as e:
        app.logger.error(f"Error communicating with the API server: {str(e)}")
        return f"Error communicating with the API server: {str(e)}"

if __name__ == '__main__':
    app.run(port=os.getenv("PORT", 5000))
