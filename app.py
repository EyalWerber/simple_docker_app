from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://db:27017/")
db = client["tasks_db"]
tasks_collection = db["tasks"]

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({"error": "Missing 'title' field"}), 400

        task = {"title": data['title'], "status": "pending"}
        result = tasks_collection.insert_one(task)
        task["_id"] = str(result.inserted_id)

        return jsonify(task), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = list(tasks_collection.find())
        for task in tasks:
            task["_id"] = str(task["_id"])  # Convert ObjectId to string
        return jsonify(tasks), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400

        updated_task = {}
        if "title" in data:
            updated_task["title"] = data["title"]
        if "status" in data:
            updated_task["status"] = data["status"]

        result = tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": updated_task})

        if result.matched_count == 0:
            return jsonify({"error": f"Task with ID {task_id} not found"}), 404

        return jsonify({"message": f"Task with ID {task_id} updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})

        if result.deleted_count == 0:
            return jsonify({"error": f"Task with ID {task_id} not found"}), 404

        return jsonify({"message": f"Task with ID {task_id} has been deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
