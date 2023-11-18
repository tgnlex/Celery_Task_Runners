from celery import *
from celery import Celery, logger, states, Task, task
from sqlite3 import User, sqlite3, process_row, connect, OperationalError
from proj import DatabaseTask
from proj.tasks import app






@app.task(base=DatabaseTask, bind=True)
def process_rows(self: task):
    for row in self.db.table.all():
        process_row(row)        

@app.task(base = DatabaseTask, serializer='json') 
def create_user(self, username, password):
    logger.info(self.request.id)
    User.objects.create(username=username, password=password)


# Upload files to a server. #
@app.task(base = DatabaseTask, bind=True)
def upload_files(self, filenames):
    logger.info(self.request.id)
    for i, file in enumerate(filenames):
        if not self.request.called_directly:
            self.update_state(state='PROGRESS',
                meta={'current': i, 'total': len(filenames)})    