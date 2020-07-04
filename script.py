import boto3
import click 
import json , time 

ec2 = boto3.client('ec2')
glue = boto3.client('glue')
iam = boto3.client('iam')


DEFAULT_USER='baymax'
DEFAULT_PASSWORD="Baymax123"

"""
Create Securtiy Group. This SG will has a self reference rule. This will be attached to all the resources
provisioned by BayMax 
"""
def createSG(vpc):
    sgExists = ec2.describe_security_groups(
        Filters=[ {
            'Name': 'group-name',
            'Values': [
                'BayMax',
            ]
        }]
    )
    if not sgExists['SecurityGroups']:
        sg = ec2.create_security_group(Description = 'This will be used by all the resources created by BayMax',
                                        GroupName='BayMax',
                                        VpcId = vpc)
        sgId =  sg['GroupId']                                                              

        selfIngress = ec2.authorize_security_group_ingress(
            GroupId=sgId,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                    'FromPort': 0,
                    'ToPort': 65535,
                    'UserIdGroupPairs': [{
                    'GroupId': sgId
                    }]
                    
                }
            ])
        selfEgress = ec2.authorize_security_group_egress(
            GroupId=sgId,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                    'FromPort': 0,
                    'ToPort': 65535,
                    'UserIdGroupPairs': [{
                    'GroupId': sgId
                    }]
                    
                }
            ])
        return sgId ; 

    else :
        return sgExists['SecurityGroups'][0]['GroupId'] 

"""
If such role Exists otherwise a create a new Role with s3Full Access & Glue Full Access
"""
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


def createDevEndpoint(glueRole,sgId,subnetId):
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

def deafultVPC():
    vpc  = ec2.describe_vpcs(
    Filters = [
        {
            'Name':'isDefault',
            'Values':["true"]
        }
        ]   
    )
    vpcId = vpc['Vpcs'][0]['VpcId']
    return vpcId

def subnetsInVpc(vpcId):
    subnets = ec2.describe_subnets(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpcId,
                ]
            },
        ]
    )
    return [subnet['SubnetId'] for subnet in subnets['Subnets']]



@click.command()
@click.option('--engine', help="Valid engine options are : redshift,aurora (for MySQL 5.6-compatible Aurora),aurora-mysql (for MySQL 5.7-compatible Aurora),aurora-postgresql,mariadb,mysql,oracle-ee,oracle-se2,oracle-se1,oracle-se,postgres,sqlserver-ee,sqlserver-se,sqlserver-ex,sqlserver-web", type=str)
@click.option('--user', help="Provide the Master User for the Database", type=str)
@click.option('--password', help="Provide the password for Master User", type=str)
@click.option('--family', help="Provide the Family for Database Engine", type=str)
@click.option('--storage', help="Specify the Amount of Storage on Database Engine")
@click.option('--vpc', help="VPC to be used for Provisioning of Resources",type=str)
@click.option('--subnet', help="Specify the Subnet", type=str)
@click.option('--version', help="Database Engine Version", type=str)
def provisioningResources(engine,vpc,user,password,family,storage,subnet,version):

    if engine is None: 
        raise Exception("engine is mandatory fields. Refer to --help for more details.")
    
    if not vpc :
        print("Launching Resources in Default Subnet")
        vpcId = deafultVPC()
    else :
        try :
            vpcExists = ec2.describe_vpcs(VpcIds=[vpc])
            if vpcExists['Vpcs'][0]['State']=='available':
                vpcId = vpc 
        except :
            print("Your provided VPC doesn't exist in your Account. launching Resources in Default VPC")
            vpcId = deafultVPC()
  
            
        
    
    # Sets the Default User & Password
    if not user:
        user = DEFAULT_USER
    if not password:
        password =DEFAULT_PASSWORD

    """
    If Subnet Id is not provided then choose the first value of subnet in the VPC list. If subnet provided but the vpc id not provided Raise an
    Exception. Proceed only when the provided subnet in the provided vpc 
    """
    vpcSubnets = subnetsInVpc(vpcId)
    if not subnet:
        subnetId = vpcSubnets[0]
    else :
        if subnet in vpcSubnets:
            subnetId = subnet
        else :
            raise Exception("provided Subnet is not in default subnet.Please provide both --vpc <vpc_id> --subnet <subnet_id>")

        
   
    
    
    sgId = createSG(vpcId) 
    print(vpcId,subnetId,sgId,user,password,engine)
    # glueRole = devEndpointRole()
    # createDevEndpoint(glueRole,sgId,subnetId)

# def provisioningResources(engine, name, master, password, family, vpc, subnet, version):
#     print(engine, name, master, password, family, vpc, subnet, version)



if __name__ == "__main__":
    provisioningResources()