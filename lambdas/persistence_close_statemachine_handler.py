import boto3
import json
import os
from common.logger_utility import *
from common.constants import *

sns = boto3.client('sns',region_name='us-west-2')
class ClosePipeline:

    def __publish_message_to_sns(self, message):
        response = sns.publish(
            TargetArn=os.environ['BATCH_NOTIFICATION_SNS'],
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )

    def __delete_sqs_message(self,event, context):
        try:
            if "queueUrl" in event[0] and "batchId" in event[0]:
                sqs = boto3.resource('sqs', region_name='us-east-1')
                queueUrl = event[0]["queueUrl"]
                receiptHandle = event[0]["receiptHandle"]
                batchId = event[0]["batchId"]
                is_historical = event[0]["is_historical"] == "true"
                persistenceQueue = os.environ['SQS_PERSISTENCE_ORCHESTRATION_QUEUE_NAME']
                if (is_historical):
                    persistenceQueue = os.environ['SQS_PERSISTENCE_ORCHESTRATION_HIS_QUEUE_NAME']
                queue = sqs.get_queue_by_name(QueueName=persistenceQueue)
                txt=json.dumps(event[0])
                if json.loads(txt).get("queueUrl") is not None:
                    message = sqs.Message(queueUrl,receiptHandle)
                    message.delete()
                    LoggerUtility.logInfo("Message deleted from sqs for batchId {}".format(batchId))
                    self.__publish_message_to_sns({"BatchId": batchId, "Status": "Persistence process completed"})
        except Exception as e:
            LoggerUtility.logError("Unable to delete sqs message for batchId {}".format(batchId))
            raise e
    
    def __push_batchid_to_nightly_sqs_queue(self, event, context):
        current_batch_id = ""
        try:
            if "batchId" in event[0]:
                sqs = boto3.resource('sqs')
                current_batch_id = event[0]["batchId"]
                nightly_queue_name = os.environ["SQS_NIGHTLY_PERSISTENCE_QUEUE_NAME"]
                nightly_batches_queue = sqs.get_queue_by_name(QueueName=nightly_queue_name)
                response = nightly_batches_queue.send_message(MessageBody=json.dumps({
                    'BatchId': current_batch_id
                }), MessageGroupId="WazeNightlyPersistenceBatchesMessageGroup")
                LoggerUtility.logInfo("Successfully pushed the message to nightly queue for batchid -"
                                      " {}".format(current_batch_id))
        except Exception as e:
            LoggerUtility.logError("Unable to delete sqs message for batchId {}".format(current_batch_id))
            raise e
    
    def close_pipeline(self, event, context):
        self.__push_batchid_to_nightly_sqs_queue(event, context)
        self.__delete_sqs_message(event, context)
