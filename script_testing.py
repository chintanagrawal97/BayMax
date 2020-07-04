import boto3
import time 
import json

ec2 = boto3.client('ec2')
glue = boto3.client('glue')
iam = boto3.client('iam')

vpc = 'vpc-0cfe4476'


# vpcExists = ec2.describe_vpcs(VpcIds=[vpc])
# if vpcExists['Vpcs'][0]['State']=='available' or vpc is None:
#     raise Exception("Check the provided VPC id")

# def createSG(vpc):
#     sgExists = ec2.describe_security_groups(
#         Filters=[ {
#             'Name': 'group-name',
#             'Values': [
#                 'BayMax',
#             ]
#         }]
#     )
#     if not sgExists['SecurityGroups']:
#         sg = ec2.create_security_group(Description = 'This will be used by all the resources created by BayMax',
#                                         GroupName='BayMax',
#                                         VpcId = vpc)
#         sgId =  sg['GroupId']                                                              

#         selfIngress = ec2.authorize_security_group_ingress(
#             GroupId=sgId,
#             IpPermissions=[
#                 {'IpProtocol': 'tcp',
#                     'FromPort': 0,
#                     'ToPort': 65535,
#                     'UserIdGroupPairs': [{
#                     'GroupId': sgId
#                     }]
                    
#                 }
#             ])
#         selfEgress = ec2.authorize_security_group_egress(
#             GroupId=sgId,
#             IpPermissions=[
#                 {'IpProtocol': 'tcp',
#                     'FromPort': 0,
#                     'ToPort': 65535,
#                     'UserIdGroupPairs': [{
#                     'GroupId': sgId
#                     }]
                    
#                 }
#             ])
#         return sgId ; 

#     else :
#         return sgExists['SecurityGroups'][0]['GroupId'] 

# sgId = createSG(vpc)    

sgId ='sg-003930dc06002b3d7'
subnetId = 'subnet-3a043a70'
# connection = glue.create_connection(
#     ConnectionInput={
#         'Name': 'BayMax',
#         'Description': 'The Connection used by BayMax',
#         'ConnectionType': 'JDBC',    
#         'ConnectionProperties': {
#                 'JDBC_CONNECTION_URL': 'jdbc:mysql://dataxxx:3306/disxxx',
#                 'USERNAME':'dummy',
#                 'PASSWORD':'dummy',
#                 'JDBC_ENFORCE_SSL': 'false',
#             },
#         'PhysicalConnectionRequirements': {
#             'SubnetId': subnet,
#             'SecurityGroupIdList': [sgId]        
#             },
#     }
# )

#Create IAM role for Glue DevEndpoint

# print(assume_role_policy_document)

# bayMaxIamRole = iam.create_role(
#     RoleName='BayMax',
#     AssumeRolePolicyDocument=assume_role_policy_document,
#     Description='This role is used by BayMax Resources'
# )

def devEndpointRole():
    try :
        response = iam.get_role(RoleName='BayMax')
        return response['Role']['Arn']
    except :
        assume_role_policy_document = json.dumps(
        {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "glue.amazonaws.com"
                ]
            },
            "Action": [
                "sts:AssumeRole"
            ]
        }]
        }
        )
        bayMaxIamRole = iam.create_role(
            RoleName = 'BayMax',
            AssumeRolePolicyDocument=assume_role_policy_document,
            Description = 'This role is used by BayMax Resources'
        )
        
        response = iam.attach_role_policy(
            RoleName='BayMax',
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
        )
        response = iam.attach_role_policy(
            RoleName='BayMax',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole'
        )
        time.sleep(3)
        
        return bayMaxIamRole['Role']['Arn']


glueRole = devEndpointRole()

print(glueRole)


devEndPoint = glue.create_dev_endpoint(
    EndpointName='BayMax',
    RoleArn=glueRole,
    SecurityGroupIds=[
        sgId,
    ],
    SubnetId=subnetId,
    WorkerType='Standard',
    NumberOfWorkers = 5 ,
    GlueVersion='1.0',
    ExtraPythonLibsS3Path='string',
    ExtraJarsS3Path='string',
    Arguments={
        'GLUE_PYTHON_VERSION': '3',
	    '--enable-glue-datacatalog': ''
    }
)
print(devEndPoint)
# print(response)


# # sg = ec2.create_security_group(Description = 'This will be used by all the resources created by BayMax', GroupName='BayMax',VpcId = vpc)
# # print(sg)

