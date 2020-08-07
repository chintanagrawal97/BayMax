####  Join dataframe 
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
    
    
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
    
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
    
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "imageembeddings", table_name = "alexnet_parquet_glue_temp", transformation_ctx = "datasource0")
    
datasource1 = glueContext.create_dynamic_frame.from_catalog(database = "default", table_name = "asin_listv2p_data_asin_list")
    
output = Join.apply(frame1 = datasource1, frame2 = datasource0, keys1 = ["asin"], keys2 = ["asin", "physical_id", "out_0000"], transformation_ctx = "join0")
    
datasink2 = glueContext.write_dynamic_frame.from_options(frame = output, connection_type = "s3", connection_options = {"path": "s3://alki-tests/glue-join-pt"}, format = "csv", transformation_ctx = "datasink2")
job.commit()
    