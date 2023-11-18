###### Celery Config File ######

# Main Settings #
broker='amqp://',
backend='rpc://',
include=['proj.tasks']
result_expires=3600,

#Time and Location Settings #
enable_utc = True,
timezone = 'Europe/London'

task_serializer='json',
accept_content=['json'],  # Ignore other content
result_serializer='json',
timezone='Europe/Oslo',
enable_utc=True,

# Set Task Type Priorities: 
task_routes = {
    'tasks.greet': 'high-priority', 
    'tasks.upload_files': 'high-priority',
    'tasks.create_user': 'high-priority',
    'tasks.get_tweets': 'medium-priority',
    'dump-context': 'medium-priority',
    'tasks.add': 'low-priority',
    'tasks.subtr': 'low-priority',
    'tasks.mul': 'low-priority',
    'tasks.divi': 'low-priority',
    'tasks.mod': 'low-priority',
    'tasks.xsum': 'low-priority'
}

task_annotations = {
    'tasks.add': {'rate_limit': '10/m'},
    'tasks.subtr': {'rate_limit': '10/m'},
    'tasks.mul': {'rate_limit': '10/m'},
    'tasks.divi': {'rate_limit': '10/m'},
    'tasks.mod': {'rate_limit': '10/m'},
    'tasks.xsum': {'rate_limit': '10/m'},
    'tasks.greet': {'rate_limit': '1/m'}
}