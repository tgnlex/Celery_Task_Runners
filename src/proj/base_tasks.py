import errno
from celery import *
from celery import Celery, renderer
from celery.exceptions import Reject
from proj import MyTask, DebugTask, logger
from os import get_file
from sqlite3 import User as User
from proj.celery import app
####################################################################################################################
############################ Base Tasks ##############################
# Base Task. #
@app.task(base=MyTask & DebugTask, autoretry_for=(Exception,), retry_backoff=True)
def x(x):
    return x

# Greeter Task . # 
@app.task(base=MyTask & DebugTask) 
def greet(self):
    logger.info(self.request.id)
    return 'Celery: Hey boss, got any tasks for me to do?'

# Dump Context Task. #
@app.task(base = MyTask & DebugTask, bind=True)
def dump_context(self):
    print('Request: {0!r}'.format(self.request))
    logger.info(self.request.id)
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
            self.request))
###############################################################################################
################# Rendering #####################################################################


############################################################################################################
########### Main Loop ######################################################################################
if __name__ == '__main__':
    args = ['worker', 'loglevel=INFO', ]
    app.worker_main(argv=args)
