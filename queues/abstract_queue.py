import boto3
import json
import logging

logger = logging.getLogger()


class AbstractQueue:
    queue_url = ''

    def __init__(self):
        self.queue = boto3.client('sqs')

    def send(self, message):
        logger.debug("########## {} Send ##########".format(self.__class__.__name__))
        if type(message) is dict:
            message = json.dumps(message)
        response = self.queue.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message
        )
        logger.debug("response: {}".format(response))
        return response

    def receive(self, max_number_of_messages=1, visibility_timeout=1, wait_time=1):
        logger.debug("########## {} Receive ##########".format(self.__class__.__name__))
        logger.debug("max_number_of_messages: {}".format(max_number_of_messages))
        logger.debug("visibility_timeout: {}".format(visibility_timeout))
        logger.debug("wait_time: {}".format(wait_time))
        response = self.queue.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_number_of_messages,
            VisibilityTimeout=visibility_timeout,
            WaitTimeSeconds=wait_time
        )
        logger.debug("response: {}".format(response))
        messages = response.get('Messages', [])
        for i in range(len(messages)):
            try:
                messages[i]["Body"] = json.loads(messages[i]["Body"])
            except:
                pass
        return messages

    def delete(self, message):
        logger.debug("########## {} Delete ##########".format(self.__class__.__name__))
        receipt_handler = message.get('ReceiptHandle', '')
        logger.debug("message_id: {}".format(receipt_handler))
        response = self.queue.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handler
        )
        logger.debug("response: {}".format(response))
        return response
