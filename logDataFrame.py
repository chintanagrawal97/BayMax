### Create Log dataframe for logging  
import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import input_file_name
import pyspark.sql.functions as func
from pyspark.sql import Row
from pyspark.sql.types import *
    
glueContext = GlueContext(sc)
spark = glueContext.spark_session
    
cSchema = StructType([StructField("jobname", StringType()) ,StructField("times-stamp", StringType()) ,StructField("log message", StringType()) ])
loglist = []
    
#loglist.append( ["myjobname"], ["2018-03-03-00:00:30"] ,["log mssage1"] )
loglist.append( ["myjobname", "2018-03-03-00:00:30" ,"log mssage1"] )
#loglist.append("myjobname,2018-03-03-00:00:31,log mssage2")
    
#log_df = spark.createDataFrame(list(map(lambda x: Row(words=x), loglist)))
#log_df.write.format("csv").mode("append").save("s3://henry-virginia/glue/csv/logoutput/")
#log_df.write.mode("append").save("s3://henry-virginia/glue/csv/logoutput/")
    
df = spark.createDataFrame(loglist,schema=cSchema)
df.write.format("csv").mode("append").save("s3://henry-virginia/glue/csv/logoutput/")
    
job.commit()