import boto3

ec2 = boto3.client('ec2')
vpc  = ec2.describe_vpcs(
    Filters = [
        {
            'Name':'isDefault',
            'Values':["true"]
        }
    ]
)
vpcId = vpc['Vpcs'][0]['VpcId']
print(vpcId)


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
subnetId = 'subnet-3a043a70'
subetIdinVPC = [subnet['SubnetId'] for subnet in subnets['Subnets']]
if subnetId in subetIdinVPC:
    print(True)