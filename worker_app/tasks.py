from __future__ import absolute_import, unicode_literals

from celery import shared_task
from datetime import timedelta
import time
# from sqs import sqs
try:
    import boto3
    import os
    import sys
    import json
except Exception as e:
    print(e)

AWS_ACCESS_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXX"
AWS_SECRET_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXX"
AWS_SQS_QUEUE_NAME = "XXXXXXXXXXXXXX"


class SQSQueue(object):
  def __init__(self, queueName=None):
      self.resource = boto3.resource('sqs', region_name='ap-south-1',
                                      aws_access_key_id=AWS_ACCESS_KEY,
                                      aws_secret_access_key=AWS_SECRET_KEY)
      self.queue = self.resource.get_queue_by_name(QueueName=AWS_SQS_QUEUE_NAME)
      self.QueueName = queueName

  def send(self, Message={}):
      data = json.dumps(Message)
      response = self.queue.send_message(MessageBody=data)
      return response

  def receive(self):
      data = {} 
      try:
          queue = self.resource.get_queue_by_name(QueueName=self.QueueName)
          for message in queue.receive_messages():
              data = message.body
              data = json.loads(data)
              message.delete()
      except Exception as e:
          print(e)
          return []
      return data


@shared_task
def add(x, y):
	print("Hello this is a task working...")
	return x + y

@shared_task
def get_message_from_sqs():
	while True:
		print("Processing the polling")
		q = SQSQueue(queueName=AWS_SQS_QUEUE_NAME)
		data = q.receive()
		print("The received from queue is:::")
		print(data)
		time.sleep(3)