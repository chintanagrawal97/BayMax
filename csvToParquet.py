### Convert  CSV to Parquet using spark 
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
    
## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
    
spark = SparkSession.builder.appName("Parquet Partition Test").getOrCreate()

df = spark.read.csv("s3://henry-virginia/glue/glue1/data1.csv")
df.show()
df.write.partitionBy('_c0').format("parquet").save("s3://henry-virginia/glue/export/")
    