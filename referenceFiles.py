'''
Glue documentation, it supports reading additional files (Ex: configuration files) using "Referenced files path" from Glue script. 
However, documentation doesn't clearly state how to read that file from the script
1. In the field itself, use the full S3 path of the file as an example: 
This will cause the file to be copied into the main directory of the Glue application, allowing Glue to reference it directly.
2. In your Spark code, you must add the file to the sparkContext to distribute the file to each worker in the cluster. This is done using:
sc.addFile('myFile.txt')
3. As each worker in the cluster will have a slightly different path for the file, we can reference it with SparkFiles when opening it 
and reading it to a variable like standard Python. 
'''

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark import SparkFiles
from awsglue.job import Job
from pyspark.sql import Row

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

print("\n*****Adding File to executors*****\n")
sc.addFile('myFile.txt')  # because the file is added to the root of the application no path should be specified, only the file name.

print("\n*****Opening File and assigning reading it to a variable*****\n")
with open(SparkFiles.get('myFile.txt')) as test_file:
    text = test_file.read()

print("\n*****Printing Contents of file*****\n")
print(text)

job.commit()