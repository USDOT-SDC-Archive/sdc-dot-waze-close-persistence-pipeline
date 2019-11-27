import os
import sys
import time
from unittest.mock import patch, MagicMock
from botocore.errorfactory import ClientError

import boto3
import pytest
from moto import mock_sqs, mock_events

from lambdas.persistence_close_statemachine_handler import ClosePipeline

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

os.environ['BATCH_NOTIFICATION_SNS'] = "batch_notification_sns"
os.environ["SQS_NIGHTLY_PERSISTENCE_QUEUE_NAME"] = "SQS_NIGHTLY_PERSISTENCE_QUEUE_NAME"


class MockSNS:
    def publish(self, *args, **kwargs):
        pass


mock_client = MockSNS()


@patch('lambdas.persistence_close_statemachine_handler.sns', mock_client)
def test_publish_message_to_sns():
    sqs_handler = ClosePipeline()
    sqs_handler.publish_message_to_sns(None)


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
def test_delete_sqs_message_no_queue_url():
    batch_id = str(int(time.time()))
    queue_events = []
    queue_event = dict()
    queue_event["batchId"] = batch_id
    queue_event["receiptHandle"] = "test"
    queue_events.append(queue_event)
    print(queue_events)
    close_pipeline_obj = ClosePipeline()
    close_pipeline_obj.delete_sqs_message(queue_events)


@mock_sqs
def test_push_batch_id_to_nightly_sqs_queue_raises_exception():
    with pytest.raises(ClientError):
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


"""
@mock_events
def test_close_pipeline():
    with pytest.raises(Exception):
        close_pipeline_obj = ClosePipeline()
        assert close_pipeline_obj.close_pipeline(None) is None
"""


def test_close_pipeline():
    close_pipeline = ClosePipeline()
    close_pipeline.push_batch_id_to_nightly_sqs_queue = MagicMock()
    close_pipeline.delete_sqs_message = MagicMock()

    close_pipeline.close_pipeline(None)
