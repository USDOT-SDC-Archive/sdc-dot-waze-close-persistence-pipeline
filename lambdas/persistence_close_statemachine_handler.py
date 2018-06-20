import boto3
import json
import os
from common.logger_utility import *
from common.constants import *

class ClosePipeline:

    def __delete_sqs_message(self,event, context):
        try:
            sqs = boto3.resource('sqs', region_name='us-east-1')
            queueUrl = event[0]["queueUrl"]
            receiptHandle = event[0]["receiptHandle"]
            batchId = event[0]["batchId"]
            persistenceQueue = os.environ['SQS_PERSISTENCE_ORCHESTRATION_QUEUE_NAME']
            queue = sqs.get_queue_by_name(QueueName=persistenceQueue)
            txt=json.dumps(event[0])
            if json.loads(txt).get("queueUrl") is not None:
                message = sqs.Message(queueUrl,receiptHandle)
                message.delete()
                LoggerUtility.logInfo("Message deleted from sqs for batchId {}".format(batchId))
        except Exception as e:
            LoggerUtility.logError("Unable to delete sqs message for batchId {}".format(batchId))
            raise e
    
    def close_pipeline(self, event, context):
        self.__delete_sqs_message(event, context)
        
