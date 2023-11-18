import logging
import celery

from celery.utils.log import get_task_logger, get_logger, logger
from logging import getLogger, LoggerAdapter, Logger
def my_task_logger():
    c_logger = celery.log.get_default_logger()
    c_logger.info('Celery Logger')
    c_t_logger = get_task_logger(__name__)
    c_t_logger.info('Task Logger')
    return c_logger, c_t_logger
def my_logger():
    logger = get_logger(__name__)
    logger.info('Logger')
    return logger
