from lambdas.persistence_close_statemachine_handler import *
from common.logger_utility import *


def lambda_handler(event, *args, **kwargs):
    LoggerUtility.set_level()
    close_pipeline_handle_event = ClosePipeline()
    close_pipeline_handle_event.close_pipeline(event)
    return event
