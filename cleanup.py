import boto3

glue = boto3.client('glue')


delDevEndpoint = glue.delete_dev_endpoint(EndpointName ='BayMax')
delConnection = glue.delete_connection(
       ConnectionName='BayMax'
    )