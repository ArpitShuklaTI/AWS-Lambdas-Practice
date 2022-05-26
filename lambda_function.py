import boto3


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    comprehend = boto3.client('comprehend')
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:280022023954:shuklaarpit'
    if event:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        try:
            file_object = s3.get_object(Bucket=bucket, Key=key)
            text = file_object["Body"].read().decode('utf-8')
            sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
            sentiment = sentiment_response["Sentiment"]
            print(sentiment_response)
            print(sentiment)
            key_phrases_response = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
            key_phrases = [phrase['Text'] for phrase in key_phrases_response['KeyPhrases']]
            print(key_phrases_response)
            print(key_phrases)
            msg = f"""
            Analysis of "{key}" file added in s3 bucket:
            Sentiment = {sentiment}
            Key Phrases = {key_phrases}
            """
            sns.publish(TopicArn = topic_arn, Message = msg)
        except Exception as e:
            print(e)
            print(f"Error getting object {key} from bucket {bucket}.")
            raise e
