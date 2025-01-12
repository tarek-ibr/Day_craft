import tkinter as tk
import ttkbootstrap as ttk
import db_functions as db
import Destroy as ds
import networkx as nx



def get_tasks(username, duration):
    user_tasks = db.get_user_tasks(username)  # Get tasks from database
    tasks = []

    time_left = int(duration)

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
    total_time = 0  # Track total time of added tasks
    queued_tasks = []

    for sorted_task in sorted_tasks:
        task_duration = int(sorted_task["task"][3])
        task_name = sorted_task["task"][1]
        prerequisite = sorted_task["prerequisite"]

        for queue in queued_tasks:
            # Check if task can be added without exceeding total allowed time
            if int(queue[3]) <= time_left and (not queue[5] or queue[5] in added_tasks) and queue[6] == 0 and queue[1] not in added_tasks:
                final_tasks.append(queue)
                total_time += int(queue[3])
                time_left -= int(queue[3])
                added_tasks.add(queue[1])

        # Check if task can be added without exceeding total allowed time
        if task_duration <= time_left and (not prerequisite or prerequisite in added_tasks) and sorted_task["task"][6]==0:
            final_tasks.append(sorted_task["task"])
            total_time += task_duration
            time_left -= task_duration
            added_tasks.add(task_name)
        else:
            if sorted_task["task"][6]==0:
                queued_tasks.append(sorted_task["task"])



        # Stop if no time is left
        if time_left <= 0:
            break

    return final_tasks



def build_task_graph_with_prerequisites(teamname):
    task_graph = nx.DiGraph()
    tasks = db.get_team_tasks(teamname)

    # Add nodes and directed edges
    for task in tasks:
        taskname = task[1]
        prerequisite = task[5]
        if task[6] == 0:
            task_graph.add_node(taskname)
            if prerequisite:
                task_graph.add_edge(prerequisite, taskname)  # prerequisite → taskname

    return task_graph


def cluster_tasks(graph):
    """
    Clusters tasks in a graph based on connected components.

    Args:
        graph (nx.DiGraph): The directed graph representing tasks and dependencies.

    Returns:
        clusters (list of sets): Each set represents a cluster of tasks.
    """
    if isinstance(graph, nx.DiGraph):
        # Use weakly connected components for directed graphs
        clusters = list(nx.weakly_connected_components(graph))
    else:
        # Use connected components for undirected graphs
        clusters = list(nx.connected_components(graph))

    return clusters


#I didn't do any thing with the duration here because I want to show all the tasks that this member should do but it's very simple to include the duration
def get_user_from_team_tasks(teamname, username, duration):
    """
    Retrieve tasks for a user from the team's tasks, grouped into clusters.

    Args:
        teamname (str): The name of the team.
        username (str): The username of the user.
        duration (int): The duration threshold for filtering tasks.

    Returns:
        list: A list of tasks assigned to the user.
    """
    # Build the task graph using the teamname
    task_graph = build_task_graph_with_prerequisites(teamname)

    # Cluster the tasks
    clusters = cluster_tasks(task_graph)

    # Dictionary to store clusters and their associated data
    cluster_dic = {}

    for cl in clusters:
        task_list = []
        total_duration = 0

        for taskname in cl:
            task = db.searchTasksByTaskname(taskname)
            if task:
                total_duration += task[3]  # Assuming task[3] is the duration
                task_list.append(task)

        cluster_dic[f"Cluster_{len(cluster_dic) + 1}"] = {
            "tasks": task_list,
            "total_duration": total_duration,
        }

    sorted_clusters = dict(sorted(cluster_dic.items(), key=lambda item: item[1]["total_duration"]))

    try:
        user_list = db.get_team_users(teamname) or []
    except Exception as e:
        print(f"Error retrieving team users: {e}")
        user_list = []

    user_task_durations = {}

    for user in user_list:
        username_of_user = user
        user_tasks = db.get_user_tasks(username_of_user)
        total_duration_user_tasks = sum(task[3] for task in user_tasks if task[6] == 0)
        user_task_durations[username_of_user] = total_duration_user_tasks

    # Sort the dictionary by total_duration_user_tasks in ascending order
    sorted_user_task_durations = dict(sorted(user_task_durations.items(), key=lambda item: item[1]))

    users_tasks = []

    for cl, dic in sorted_clusters.items():
        task_list = dic["tasks"]
        duration = dic["total_duration"]

        # Assign tasks to the user with the lowest total duration
        user_with_lowest_duration = next(iter(sorted_user_task_durations))
        users_tasks.append((user_with_lowest_duration, task_list))

        # Update the user's total duration
        sorted_user_task_durations[user_with_lowest_duration] += duration

        # Re-sort the dictionary after updating
        sorted_user_task_durations = dict(sorted(sorted_user_task_durations.items(), key=lambda item: item[1]))

    user_of_team_tasks = []
    #total_duration = 0
    for n, t in users_tasks:
        # for ta in t:
        #     total_duration += ta[3]
        # if n == username and total_duration<=duration:
        if n == username:
            for ta in t:
                user_of_team_tasks.append(ta)

    return user_of_team_tasks
