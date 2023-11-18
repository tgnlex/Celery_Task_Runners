import celery
from celery import app_or_default, Task, logger
from sqlite3 import sqlite3, process_row, connect, OperationalError


class Scheduler:
    def __init__(self, app):
        self.app = app_or_default(app)
        self.schedule = {}
        return app
    
# Base Task. #
class MyTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info('Task: {task_id} failed! \n'
                    'Arguments:' *args, '\n', 
                    'Keyword Arguments:' **kwargs, '\n', 
                    'Error Info:' *einfo, '\n')
        print('Task failed: {0!r}'.format(task_id, exc, einfo))
    def on_success(self, retval, task_id, args, kwargs):
        logger.info('Task: {task_id} succeeded! \n'
                    'Arguments:' *args, '\n', 
                    'Keyword Arguments:' **kwargs, '\n', 
                    'Return Value' **retval, '\n')
        print('Task succeeded: {0!r}'.format(task_id))

class HttpError(Exception):
    def __init__(self, status_code, headers=None, body=None):
        self.status_code = status_code
        self.headers = headers
        self.body = body

        super(HttpError, self).__init__(status_code, headers, body)
        
class NaiveAuthenticateServer(Task):
    def __init__(self):
        self.users = {'george': 'password'}

    def run(self, username, password):
        try:
            return self.users[username] == password
        except KeyError:
            return False

# Base Task with Retry. #
class BaseTaskWithRetry(Task):
    autoretry_for = (TypeError,)
    max_retries = 5
    retry_backoff = True
    retry_backoff_max = 700
    retry_jitter = False
    
# Debug Task. #
class DebugTask(Task):
    def __call__(self, *args, **kwargs):
        print('STARTING TASK: {0.name}[{0.request.id}]'.format(self))
        return self.run(*args, **kwargs)
    
# Database Tasks #
class DatabaseTask(Task):
    _db = None
    @property
    def db(self):
        if self._db is None:
            self._db = sqlite3.connect()
        return self._db