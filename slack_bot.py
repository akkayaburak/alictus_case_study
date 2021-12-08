from flask import Flask, request
from google_drive_api import connect, search_file, calculate_budget
app = Flask(__name__)


@app.route('/calculate_budget', methods=['POST'])
def budget():
    file_name = request.form['text']
    service = connect()
    file_id = search_file(service=service, file_name=file_name)

    return str(calculate_budget(service, file_id))


if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
