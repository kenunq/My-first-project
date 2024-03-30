from HomePage.services import send_problem
from mysite.celery import app


@app.task
def send_problem_message(files, text):
    send_problem(files, text)

