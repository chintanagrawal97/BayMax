import boto3
import random
from botocore.exceptions import ClientError

"""
Confirm whether everything is being provisioned in the default vpc ? right ?Thsi also required DBSubnetGroupName which 
I guess prbably requires you to add some subnets then resources will be launched their I guess
"""

"""
We will be asking engineers to give i/p via --enginer <> .So better to do a string match on that
--engine aurora,postgres,oracle,sqlserver,mysql
then after auroror --> Give out these declarations 
    print("select the type of Amazon Aurora instance")
    print("1 - aurora (for MySQL 5.6-compatible Aurora)")
    print("2 - aurora-mysql (for MySQL 5.7-compatible Aurora)")

I was thinking of using the name BayMax as the single identifier. It will them to easily filter the resource and for us to delete them too using cleanup script.
Also we can give a warinng hey u already have a running resource , better to run the cleanup script then provision or you can give your identifier too 
So I think removeg the Hash 

Also there should be a much easier option where they don't have to give the required detils too and can
simpli proceed wuth the default cluster creation template that we have provision ?
"""
   
SGId = "sg-003930dc06002b3d7"
hash = str(random.getrandbits(128))
MasterUsername = 'postgres'
MasterUserPassword = 'admin123'
3
def numbers_to_aurora_engines(argument):
    switcher = {
        1: "aurora",
        2: "aurora-mysql",
        3: "aurora-postgresql"
    }
    return switcher.get(argument, "Please select a number within a range")

def numbers_to_oracle_engines(argument):
    switcher = {
        1: "oracle-ee",
        2: "oracle-se2",
        3: "oracle-se1",
        4: "oracle-se"
    }
    return switcher.get(argument, "Please select a number within a range")

def numbers_to_mssql_engines(argument):
    switcher = {
        1: "sqlserver-ee",
        2: "sqlserver-se",
        3: "sqlserver-ex",
        4: "sqlserver-web"
    }
    return switcher.get(argument, "Please select a number within a range")


if __name__ == "__main__":

    rds = boto3.client('rds',region_name='us-east-1')

    print("Select the DBEngine")
    print("1 - Amazon-Aurora")
    print("2 - MySQL")
    print("3 - PostgreSQL")
    print("4 - Oracle")
    print("5 - Microsoft SQL Server")
    DBEngine = int(input())
# Aurora doesn't take input like publically accesible valla ?
    if DBEngine == 1:
        print("select the type of Amazon Aurora instance")
        print("1 - aurora (for MySQL 5.6-compatible Aurora)")
        print("2 - aurora-mysql (for MySQL 5.7-compatible Aurora)")
        print("3 - aurora-postgresql")
        DBEngine_type = int(input())
        DB = numbers_to_aurora_engines(DBEngine_type)

        try:

            response = rds.create_db_cluster(
            DatabaseName='BayMax'+hash,
            DBClusterIdentifier='BayMax'+hash,
            VpcSecurityGroupIds=[
                SGId,
            ],
            DBSubnetGroupName='default',
            Engine=DB,
            MasterUsername=MasterUsername,
            MasterUserPassword=MasterUserPassword)

        except ClientError as e:
            print(e)

    elif DBEngine == 2:

# botocore.exceptions.ParamValidationError: Parameter validation failed:
# Invalid type for parameter MultiAZ, value: True, type: <class 'str'>, valid types: <class 'bool'>
# Invalid type for parameter PubliclyAccessible, value: False, type: <class 'str'>, valid types: <class 'bool'>

        MultiAZ  = input('Want MultiAZ if yes then give True else False:    ')
        PubliclyAccessible = input('Want PubliclyAccessible if yes then give True else False:     ')
        AllocatedStorage = int(input('Enter the amount storage you want to allocate to DB in GBs:    '))

        try:

            response = rds.create_db_instance(
            DBName='BayMax'+hash,
            DBInstanceIdentifier='BayMax'+hash,
            DBInstanceClass='db.m5.xlarge',
            Engine='mysql',
            MasterUsername=MasterUsername,
            MasterUserPassword=MasterUserPassword,
            VpcSecurityGroupIds=[
                SGId,
            ],
            DBSubnetGroupName='default',
            MultiAZ=MultiAZ,
            PubliclyAccessible=PubliclyAccessible,
            AllocatedStorage=AllocatedStorage)

        except ClientError as e:
            print(e)
#
# PostGres input is not working . Its taking in argumnets as string rather it should be boolean
# 
# 

    elif DBEngine == 3:

        MultiAZ  = input('Want MultiAZ if yes then give True else False:    ')
        PubliclyAccessible = input('Want PubliclyAccessible if yes then give True else False:     ')
        AllocatedStorage = int(input('Enter the amount storage you want to allocate to DB in GBs:    '))

        try:

            response = rds.create_db_instance(
            DBName='BayMax'+hash,
            DBInstanceIdentifier='BayMax'+hash,
            DBInstanceClass='db.m5.xlarge',
            Engine='postgres',
            MasterUsername=MasterUsername,
            MasterUserPassword=MasterUserPassword,
            VpcSecurityGroupIds=[
                SGId,
            ],
            DBSubnetGroupName='default',
            MultiAZ=MultiAZ,
            PubliclyAccessible=PubliclyAccessible,
            AllocatedStorage=AllocatedStorage)

        except ClientError as e:
            print(e)

    elif DBEngine == 4:


        print("select the type of Amazon Aurora instance")
        print("1 - oracle-ee (Oracle Database Enterprise Edition (EE))")
        print("2 - oracle-se2 (Oracle Database Standard Edition Two (SE2))")
        print("3 - oracle-se1 (Oracle Database Standard Edition One (SE1))")
        print("4 - oracle-se (Oracle Database Standard Edition (SE))")
        DBEngine_type = int(input())
        DB = numbers_to_oracle_engines(DBEngine_type)
        MultiAZ  = input('Want MultiAZ if yes then give True else False:    ')
        PubliclyAccessible = input('Want PubliclyAccessible if yes then give True else False:     ')
        AllocatedStorage = int(input('Enter the amount storage you want to allocate to DB in GBs:    '))

        try:

            response = rds.create_db_instance(
            DBName='BayMax'+hash,
            DBInstanceIdentifier='BayMax'+hash,
            DBInstanceClass='db.m5.xlarge',
            Engine='oracle-ee',
            MasterUsername=MasterUsername,
            MasterUserPassword=MasterUserPassword,
            VpcSecurityGroupIds=[
                SGId,
            ],
            DBSubnetGroupName='default',
            MultiAZ=MultiAZ,
            PubliclyAccessible=PubliclyAccessible,
            AllocatedStorage=AllocatedStorage,
            LicenseModel='bring-your-own-license')
            print('Oracle DB in here is created using bring-your-own-license. Hence, if you would like to change the license please feel free to use modfiy instance option and change and for more info checkout: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Oracle.html')

        except ClientError as e:
            print(e)

    elif DBEngine == 5:

        print("select the type of Amazon Aurora instance")
        print("1 - sqlserver-ee (Enterprise)")
        print("2 - sqlserver-se (Standard)")
        print("3 - sqlserver-ex (Express)")
        print("4 - sqlserver-web (Web)")
        DBEngine_type = int(input())

        if DBEngine_type == 3:
            DBInstanceClass = "db.t3.xlarge"
        else:
            DBInstanceClass = "db.m5.xlarge"


        DB = numbers_to_mssql_engines(DBEngine_type)

        MultiAZ  = input('Want MultiAZ if yes then give True else False:    :    ')
        PubliclyAccessible = input('Want PubliclyAccessible if yes then give True else False:     ')
        AllocatedStorage = int(input('Enter the amount storage you want to allocate to DB in GBs:    '))

        try:
            response = rds.create_db_instance(
            DBInstanceIdentifier='BayMax'+hash,
            DBInstanceClass=DBInstanceClass,
            Engine=DB,
            MasterUsername=MasterUsername,
            MasterUserPassword=MasterUserPassword,
            VpcSecurityGroupIds=[
                SGId,
            ],
            DBSubnetGroupName='default',
            MultiAZ=MultiAZ,
            PubliclyAccessible=PubliclyAccessible,
            AllocatedStorage=AllocatedStorage,
            LicenseModel='license-included')

        except ClientError as e:
            print(e)
