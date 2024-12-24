#!/bin/bash

# Base URL of the Flask app
BASE_URL="http://127.0.0.1:5000/tasks"

# 1. Create a new task
echo "Creating a new task..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL" \
    -H "Content-Type: application/json" \
    -d '{"title": "My First Task"}')
echo "Response: $CREATE_RESPONSE"

# Extract task ID from the response
TASK_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

if [[ -z "$TASK_ID" ]]; then
    echo "Failed to create a task!"
    exit 1
fi
echo "Created task with ID: $TASK_ID"

# 2. Get all tasks
echo "Getting all tasks..."
ALL_TASKS=$(curl -s -X GET "$BASE_URL")
echo "All tasks: $ALL_TASKS"

# 3. Update the task
echo "Updating task with ID $TASK_ID..."
UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/$TASK_ID" \
    -H "Content-Type: application/json" \
    -d '{"title": "Updated Task", "status": "completed"}')
echo "Response: $UPDATE_RESPONSE"

# 4. Delete the task
echo "Deleting task with ID $TASK_ID..."
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/$TASK_ID")
echo "Response: $DELETE_RESPONSE"

# 5. Verify the task has been deleted
echo "Getting all tasks again..."
ALL_TASKS_AFTER_DELETE=$(curl -s -X GET "$BASE_URL")
echo "All tasks after deletion: $ALL_TASKS_AFTER_DELETE"
