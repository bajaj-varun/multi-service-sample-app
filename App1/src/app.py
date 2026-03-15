from flask import Flask, jsonify
from tasks import process_app1_task

app = Flask(__name__)

@app.route('/health_check')
def health_check():
    return jsonify({"status": "App1 is healthy"})

@app.route('/do_task')
def do_task():
    task = process_app1_task.delay("Task from App1")
    return jsonify({"task_id": task.id, "status": "Task dispatched"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
