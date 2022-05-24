import boto3


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    if event:
        print(f"Event: {event}")
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print(f"File {key} uploaded in bucket {bucket}")
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            print(f"Response: {response}")
            file_content = response["Body"].read().decode('utf-8')
            print(f"File content: {file_content}")
        except Exception as e:
            print(e)
            print(f"Error getting object {key} from bucket {bucket}.")
            raise e
