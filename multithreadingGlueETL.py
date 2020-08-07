===========================================
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import logging
import threading
import time

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

def thread_function(name):
    logging.info("Thread %s: starting", name)
    datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "4thmay", table_name = "testingdefaultpartition", transformation_ctx = "datasource0")
    datasource0.show()
    time.sleep(2)
    logging.info("Thread %s: finishing", name)
    
    
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
threads = list()

for index in range(3):
    logging.info("Main    : create and start thread %d.", index)
    x = threading.Thread(target=thread_function, args=(index,))
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    logging.info("Main    : before joining thread %d.", index)
    thread.join()
    logging.info("Main    : thread %d done", index)

job.commit()
==============================================