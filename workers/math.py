from celery import Celery, logger, states, Task, task 
from proj.tasks import MyTask, DebugTask, app

@app.task(base=MyTask)
def add(self, x, y):
    logger.info(self.request.id)
    return x + y

# Multiply two variables. #
@app.task(base=MyTask & DebugTask) 
def mul(self, x, y):
    logger.info(self.request.id)
    return x * y

# Subtract two variables. #
@app.task(base=MyTask & DebugTask) 
def subtr(self, x, y):
    logger.info(self.request.id)
    return x - y

# Divide two variables. #
@app.task(base=MyTask & DebugTask)
def divi(self, x, y):
    logger.info(self.request.id)
    return x / y

# Modulo two variables. #
@app.task(base=MyTask & DebugTask)
def mod(self, x, y):
    logger.info(self.request.id)
    return x % y

# Sum a list of numbers. #
@app.task(base=MyTask & DebugTask)
def xsum(self, numbers):
    logger.info(self.request.id)
    return sum(numbers)