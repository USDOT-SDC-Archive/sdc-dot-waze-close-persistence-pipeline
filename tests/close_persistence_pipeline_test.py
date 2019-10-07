from moto import mock_sns, mock_sqs, mock_events
import sys
import os
import time
import pytest
import boto3
from lambdas.persistence_close_statemachine_handler import ClosePipeline
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


@mock_sns
def test_publish_message_to_sns():
    batch_id = str(int(time.time()))
    topic_name = "dev-dot-sdc-cloudwatch-alarms-notification-topic"
    message = {"BatchId": batch_id, "Status": "Persistence process completed"}
    sns = boto3.client('sns', region_name='us-east-1')
    response = sns.create_topic(Name=topic_name)
    os.environ["BATCH_NOTIFICATION_SNS"] = response['TopicArn']
    close_pipeline_obj = ClosePipeline()
    close_pipeline_obj.publish_message_to_sns(message)
    assert True


@mock_sqs
def test_delete_sqs_message():
    with pytest.raises(Exception):
        batch_id = str(int(time.time()))
        sqs = boto3.client('sqs', region_name='us-east-1')
        response = sqs.create_queue(QueueName='dev-dot-sdc-waze-data-persistence-orchestration',
                                    Attributes={'FifoQueue': "false", 'DelaySeconds': "60",
                                                'MaximumMessageSize': "262144", 'MessageRetentionPeriod': "1209600",
                                                'VisibilityTimeout': "960"})
        queue_url = response['QueueUrl']
        queue_events = []
        queue_event = dict()
        queue_event["batchId"] = batch_id
        queue_event["queueUrl"] = queue_url
        queue_event["receiptHandle"] = "test"
        queue_events.append(queue_event)
        print(queue_events)
        close_pipeline_obj = ClosePipeline()
        close_pipeline_obj.delete_sqs_message(queue_events)


@mock_sqs
def test_push_batch_id_to_nightly_sqs_queue_raises_exception():
    with pytest.raises(Exception):
        sqs = boto3.client('sqs', region_name='us-east-1')
        sqs.create_queue(QueueName='dev-dot-sdc-waze-data-nightly-elt.fifo',
                         Attributes={'FifoQueue': "true", 'DelaySeconds': "5", 'MaximumMessageSize': "262144",
                                     'MessageRetentionPeriod': "1209600", 'VisibilityTimeout': "960",
                                     'ContentBasedDeduplication': "true"})
        generated_batch_id = str(int(time.time()))
        queue_events = []
        queue_event = dict()
        queue_event["batchId"] = generated_batch_id
        queue_events.append(queue_event)
        close_pipeline_obj = ClosePipeline()
        close_pipeline_obj.push_batch_id_to_nightly_sqs_queue(queue_events)


@mock_sqs
def test_push_batch_id_to_nightly_sqs_queue():
    sqs = boto3.client('sqs', region_name='us-east-1')
    response = sqs.create_queue(QueueName='dev-dot-sdc-waze-data-nightly-elt.fifo',
                                Attributes={'FifoQueue': "true", 'DelaySeconds': "5", 'MaximumMessageSize': "262144",
                                            'MessageRetentionPeriod': "1209600", 'VisibilityTimeout': "960",
                                            'ContentBasedDeduplication': "true"})
    queue_url = response['QueueUrl']

    queue_name = queue_url[queue_url.rfind('/') + 1: len(queue_url)]
    os.environ['SQS_NIGHTLY_PERSISTENCE_QUEUE_NAME'] = queue_name
    generated_batch_id = str(int(time.time()))
    queue_events = []
    queue_event = dict()
    queue_event["batchId"] = generated_batch_id
    queue_events.append(queue_event)
    close_pipeline_obj = ClosePipeline()
    close_pipeline_obj.push_batch_id_to_nightly_sqs_queue(queue_events)
    assert True


@mock_events
def test_close_pipeline():
    with pytest.raises(Exception):
        close_pipeline_obj = ClosePipeline()
        assert close_pipeline_obj.close_pipeline(None) is None
