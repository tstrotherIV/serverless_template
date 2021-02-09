import boto3
import datetime
import logging
import uuid
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()


class AbstractModel:
    table_name = ''

    def __init__(self):
        database = boto3.resource('dynamodb')
        self.table = database.Table(self.table_name)

    def get(self, item_id):
        logger.debug("########## {} Get ##########".format(self.__class__.__name__))
        logger.debug("item_id: {}".format(item_id))

        key = Key('id').eq(item_id)
        items = self.table.query(KeyConditionExpression=key).get('Items')
        item = items[0] if items else {}

        logger.debug("return: {}".format(item))

        return item

    def insert(self, item):
        item = item.copy()
        logger.debug("########## {} Insert ##########".format(self.__class__.__name__))
        logger.debug("item: {}".format(item))

        if item.get('id') is None:
            item['id'] = str(uuid.uuid4())
        item['created_on'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.table.put_item(Item=item)

        logger.debug("return: {}".format(item))

        return item

    def update(self, item_id, updated_item):
        logger.debug("########## {} Update ##########".format(self.__class__.__name__))
        logger.debug("item_id: {}".format(item_id))
        logger.debug("updated_item: {}".format(updated_item))

        item = self.get(item_id)
        item['updated_on'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for key, value in updated_item.items():
            item[key] = value
        self.table.put_item(Item=item)

        logger.debug("return: {}".format(item))

        return item

    def delete(self, item_id):
        logger.debug("########## {} Delete ##########".format(self.__class__.__name__))
        logger.debug("item_id: {}".format(item_id))
        try:
            self.table.delete_item(Key={'id': item_id})
        except Exception as e:
            logger.critical("########## {} Error: {}".format(self.__class__.__name__, str(e)))
            return False
        return True

    def get_all_by_index(self, index, value):
        logger.debug("########## {} - Get All By Index ##########".format(self.__class__.__name__))
        logger.debug("index: {}".format(index))
        logger.debug("value: {}".format(value))

        key = Key(index).eq(value)
        response = self.table.query(IndexName=index + '_index', KeyConditionExpression=key)
        items = response.get('Items')
        while 'LastEvaluatedKey' in response:
            response = self.table.query(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.append(response['Items'])
        return items
