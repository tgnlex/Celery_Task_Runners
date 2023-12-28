from celery import Celery
from celery.utils.log import get_task_logger, get_logger,
logger = get_task_logger(__name__)

app = Celery('proj', 
            broker='amqp://', 
            backend='rpc://', 
            log='proj.logger', 
            include=['proj.base_tasks', 
                      'workers.db',
                      'workers.twitter',
                      'workers.math', 
                      'workers.http'
                     ],  
            task_cls='proj.classes:MyTask')
app.config_from_object('celeryconfig')

class MyCelery(Celery):
    def gen_task_name(self, name, module):
        if module.endswith('.tasks'):
            module = module[:-6]
        return super().gen_task_name(name, module)



if __name__ == '__main__':
    app.start()