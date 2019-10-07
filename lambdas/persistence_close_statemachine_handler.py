import boto3
import json
from common.logger_utility import *
sns = boto3.client('sns', region_name='us-east-1')


class ClosePipeline:

    def publish_message_to_sns(self, message):
        sns.publish(
            TargetArn=os.environ['BATCH_NOTIFICATION_SNS'],
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )

    def delete_sqs_message(self, event):
        batch_id = ""
        try:
            if "queueUrl" in event[0] and "batchId" in event[0]:
                sqs = boto3.resource('sqs', region_name='us-east-1')
                queue_url = event[0]["queueUrl"]
                receipt_handle = event[0]["receiptHandle"]
                batch_id = event[0]["batchId"]
                txt = json.dumps(event[0])
                if json.loads(txt).get("queueUrl") is not None:
                    message = sqs.Message(queue_url, receipt_handle)
                    message.delete()
                    LoggerUtility.logInfo("Message deleted from sqs for batchId {}".format(batch_id))
                    self.publish_message_to_sns({"BatchId": batch_id, "Status": "Persistence process completed"})
        except Exception as e:
            LoggerUtility.logError("Unable to delete sqs message for batchId {}".format(batch_id))
            raise e
    
    def push_batch_id_to_nightly_sqs_queue(self, event):
        current_batch_id = ""
        try:
            if "batchId" in event[0]:
                sqs = boto3.resource('sqs', region_name='us-east-1')
                current_batch_id = event[0]["batchId"]
                nightly_queue_name = os.environ["SQS_NIGHTLY_PERSISTENCE_QUEUE_NAME"]
                nightly_batches_queue = sqs.get_queue_by_name(QueueName=nightly_queue_name)
                response = nightly_batches_queue.send_message(MessageBody=json.dumps({
                    'BatchId': current_batch_id
                }), MessageGroupId="WazeNightlyPersistenceBatchesMessageGroup")
                LoggerUtility.logInfo("Successfully pushed the message to nightly queue for batchid -"
                                      " {} with response - {}".format(current_batch_id, response))
        except Exception as e:
            LoggerUtility.logError("Unable to push sqs message to nightly queue for batchId {}".format(current_batch_id))
            raise e
    
    def close_pipeline(self, event):
        self.push_batch_id_to_nightly_sqs_queue(event)
        self.delete_sqs_message(event)
