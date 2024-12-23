import tkinter as tk
import ttkbootstrap as ttk
import db_functions as db
import Destroy as ds


def get_tasks(username, duration):
    user_tasks = db.get_user_tasks(username)  # Get tasks from database
    tasks = []

    for task in user_tasks:
        if int(task[3]) <= int(duration):  # Filter tasks based on duration
            tasks.append(task)

    # Step 1: Build a dictionary for prerequisites if present
    task_dic = {}
    for task in tasks:
        task_name = task[1]
        task_duration = int(task[3])
        task_priority = int(task[2])
        task_dic[task_name] = {
            "task": task,
            "score": task_priority / task_duration if task_duration > 0 else 0,  # Avoid division by zero
            "prerequisite": task[5]  # Assuming task[5] is the prerequisite
        }

    # Step 2: Sort tasks by score in descending order
    sorted_tasks = sorted(task_dic.values(), key=lambda x: x["score"], reverse=True)

    final_tasks = []
    added_tasks = set()  # Track added task names to ensure prerequisites are respected

    for sorted_task in sorted_tasks:
        task_name = sorted_task["task"][1]
        prerequisite = sorted_task["prerequisite"]

        # Add task if it has no prerequisite or its prerequisite is already in the list
        if not prerequisite or prerequisite in added_tasks:
            final_tasks.append(sorted_task["task"])
            added_tasks.add(task_name)

    return final_tasks

def get_shortest_path_to_tasks(username, duration):
    pass