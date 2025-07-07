from typing import List, Dict
from celery import Celery
from io import StringIO
from time import time
import csv
import os


celery_app = Celery("tasks", broker="redis://redis:6379/0")

@celery_app.task(name="export_task_to_csv")
def export_tasks_to_csv(tasks: List[Dict], user_id: int):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Title", "Description", "Completed", "Due Date", "Created At", "Priority"])
    for task in tasks:
        writer.writerow([task["id"], task["title"], task["description"], task["completed"], task["due_date"], task["created_at"], task["priority"]])

    filename = f"task_export_user_{user_id}_{str(time())}.csv"
    export_path = os.path.join("exports", filename)

    os.makedirs("exports", exist_ok=True)
    with open(export_path, "w", encoding="utf-8") as f:
        f.write(output.getvalue())

    output.close()
    print(f"Exported tasks to {export_path}")

# @celery_app.task(name="export_task_to_json")
# def export_task_to_json(task):
#     pass
