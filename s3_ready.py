def s3_handler(s, event):

    audit_role = 'arn:aws:iam::'+str(account)+':role/OrganizationAccountAccessRole'

    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn=audit_role,
        RoleSessionName='cross_acct_lambda'
    )

    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    # create service client using the assumed role credentials, e.g. S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    response = s3.get_object(Bucket=bucket, Key=key)
    # print("CONTENT TYPE: " + response['ContentType'])
    # return response['ContentType']
    body = response['Body']
    data = body.read()

    structured_logs = []