from flask import Flask, jsonify, request, render_template
import uuid

app = Flask(__name__)

# using in memory database for simplicity
tasks = {}

# endpoint to retrieve tasks
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        'title': data['title'],
        'description': data['description'],
        'completed': False
    }
    return jsonify({'id': task_id}), 201

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    if task_id in tasks:
        tasks[task_id].update({
            'title': data['title'],
            'description': data['description'],
            'completed': data['completed']
        })
        return jsonify(tasks[task_id])
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({'message': 'Deleted'})
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
