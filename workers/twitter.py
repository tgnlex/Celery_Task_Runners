from celery import Celery, states, Ignore , Task, chain,  xstarmap, chunks, group, xmap, group
from twitter import Twitter, FailWhaleError, LoginError
app = Celery('proj', broker='amqp://', backend='rpc://', include=['proj.tasks'])
app.config_from_object('../celeryconfig')
app.task = Task

@app.task(bind=True)
def send_twitter_status(self, oauth, tweet):
    try: 
        twitter = Twitter(oauth)
        twitter.update_status(tweet)
    except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
        raise self.retry(exc=exc, countdown=60, max_retries=3)

# Get the timeline of a user. #
@app.task(bind=True)
def get_tweets(self, user):
    timeline = Twitter.get_timeline(user)
    if not self.request.called_directly:
        self.update_state(state=states.SUCCESS, meta=timeline)
    raise Ignore()

# Refresh the timeline of a user. #
@app.task
def refresh_timeline(user):
    try:
        Twitter.refresh_timeline(user)
    except FailWhaleError as exc:
        raise refresh_timeline.retry(exc=exc, max_retries=5)