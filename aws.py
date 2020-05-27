import boto3
import settings
client = boto3.client('sns')

def publish_notification(product_name, product_url, product_id):
    print('Notifying about product_id {}'.format(product_id))
    response = client.publish(
        TopicArn=settings.SNS_EU_WEST_ARN_FORMAT.format(product_id),
        Message=settings.SNS_MESSAGE_IN_STOCK_STRING.format(product_name, product_url),
        MessageAttributes={
            'string': {
                'DataType': 'String',
                'StringValue': 'string',
            }
        }
    )
    print(response)

