

import time
import os

from google.cloud import pubsub
from oauth2client.service_account import ServiceAccountCredentials

project_id = 'universalclockandweather'  # Enter your project ID here
topic_name = 'weather'  # Enter your topic name here
subscription_name = 'my_subscription123'  # Can be whatever, but must be unique (for the topic?)
service_account_json = 'UniversalClockAndWeather-d07ba0b7dfb9.json' # Location of the server service account credential file


def on_message(message):
    """Called when a message is received"""
    print('Received message: {}'.format(message))
    message.ack()


# Ugly hack to get the API to use the correct account file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_json

# Create a pubsub subscriber
subscriber = pubsub.SubscriberClient()

topic = 'projects/{project_id}/topics/{topic}'.format(
    project_id=project_id,
    topic=topic_name,
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=project_id,
    sub=subscription_name,
)

# Try to delete the subscription before creating it again
try:
    subscriber.delete_subscription(subscription_name)
except: # broad except because who knows what google will return
    # Do nothing if fails
    None

# Create subscription
subscription = subscriber.create_subscription(subscription_name, topic)

# Subscribe to subscription
print "Subscribing"
subscriber.subscribe(subscription_name, callback=on_message)

# Keep the main thread alive
while True:
    time.sleep(100)
