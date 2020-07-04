import boto3

# sgId ='sg-003930dc06002b3d7'
sgId ='sg-003930dc06002b3d7'
subnetId = 'subnet-3a043a70'
vpc = 'vpc-0f5de45e82534b8ea'
user = 'baymax'
password ='Baymax123'
redshift = boto3.client('redshift')


def createRedshift(user,password,vpc,sgId):
    response = redshift.create_cluster(
        DBName='bay-max',
        ClusterIdentifier='BayMax',
        ClusterType='single-node',
        NodeType='dc2.large',
        MasterUsername=user,
        MasterUserPassword=password,
        VpcSecurityGroupIds=[
           sgId,
        ],
        Port=5439,
        AllowVersionUpgrade=True,
        PubliclyAccessible=True,
    )
    return response

cluster = createRedshift(user,password,vpc,sgId)
print(cluster)