from flask import Flask, jsonify
import requests
import os
from tasks import process_app3_task

app = Flask(__name__)

APP2_URL = os.environ.get("APP2_URL", "http://app2.default.svc.cluster.local:5002")

@app.route('/health_check')
def health_check():
    return jsonify({"status": "App3 is healthy"})

@app.route('/call_app2_health_check')
def call_app2_health_check():
    try:
        response = requests.get(f'{APP2_URL}/health_check', timeout=5)
        return jsonify({"app2_response": response.json(), "status": "Success"})
    except requests.RequestException as e:
        return jsonify({"error": str(e), "status": "Failed"}), 500

@app.route('/do_task')
def do_task():
    task = process_app3_task.delay("Task from App3")
    return jsonify({"task_id": task.id, "status": "Task dispatched"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
