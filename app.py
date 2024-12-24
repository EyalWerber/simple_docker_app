from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []  # In-memory storage for tasks

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        if not data or 'title' not in data:  # Ensure 'title' is provided
            return jsonify({"error": "Missing 'title' field"}), 400

        task = {"id": len(tasks) + 1, "title": data['title'], "status": "pending"}
        tasks.append(task)
        return jsonify(task), 201  # Return the created task

    except Exception as e:  # Catch any unexpected exceptions
        return jsonify({"error": str(e)}), 500



@app.route('/tasks/<int:task_id>',methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error":"Missing request body"}),400
        for task in tasks:
            if task['id'] == task_id:
                task['title'] = data.get('title',task['title'])
                task['status'] = data.get('status', task['status'])
                return jsonify(task),200
        return jsonify({"error": f"Task with ID {task_id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE: Delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        # Find the task with the matching ID
        global tasks
        updated_tasks = [task for task in tasks if task['id'] != task_id]

        if len(updated_tasks) == len(tasks):
            return jsonify({"error": f"Task with ID {task_id} not found"}), 404

        tasks = updated_tasks
        return jsonify({"message": f"Task with ID {task_id} has been deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
