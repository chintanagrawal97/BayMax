When possible, retrieve the credentials directly from the connection definition in the AWS Glue Data Catalog. To retrieve the credentials using AWS CLI, run the get-connection command. Example:

$ aws glue get-connection --catalog-id 111122223333 --name ConnectToRDS

You can also retrieve the credentials using the extract_jdbc_conf GlueContext Class. Example:

glueContext.extract_jdbc_conf('ConnectToRDS')

Troubleshoot connection errors

If you create a JDBC connection to your data store and use that connection in your AWS Glue job, the job will inherit a subnet that does not allow AWS Glue to communicate with Secrets Manager. When this happens, your job fails with an error message similar to the following:

com.amazonaws.SdkClientException Unable to execute HTTP request: Connect to secretsmanager.us-east-2.amazonaws.com:443 [secretsmanager.us-east-2.amazonaws.com/18.218.193.134,
    secretsmanager.us-east-2.amazonaws.com/18.220.47.208, secretsmanager.us-east-2.amazonaws.com/18.220.50.148, secretsmanager.us-east-2.amazonaws.com/2600:1f16:abc:7c02:6a81:b832:6260:d612, secretsmanager.us-east-2.amazonaws.com/2600:1f16:abc:7c00:d05e:6dce:1e7:9921,
    secretsmanager.us-east-2.amazonaws.com/2600:1f16:abc:7c01:1dae:b53d:e4d1:e46b] failed: Network is unreachable (connect failed)

To resolve connection errors:

1.   Create an Amazon Virtual Private Cloud (Amazon VPC) interface endpoint for Secrets Manager. AWS Glue will use this endpoint to communicate with Secrets Manager. For more information, see How to connect to AWS Secrets Manager service within a Virtual Private Cloud.

2.    Attach the SecretsManagerReadWrite AWS Identity and Access Management (IAM) policy to the GlueServiceRole. The policy grants the role permission to authenticate Secrets Manager and retrieve the secrets. For more information about permissions for Secrets Manager, see Authentication and Access Control for AWS Secrets Manager.

3.    Create an AWS Glue job using code similar to the following. This job tests connectivity from either your Zeppelin Notebook or your ETL job. This job also adds a connection from your ETL job to the desired database.

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

import boto3
import base64
import json
from botocore.exceptions import ClientError

print "start boto3 client"
client = boto3.client(
    "secretsmanager",
    region_name="ap-southeast-2"
)
 
print "retrieving secret"
get_secret_value_response = client.get_secret_value(
    SecretId="test"
)
dbsecret = json.loads(get_secret_value_response['SecretString'])
 
## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
 
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
 
job.commit()