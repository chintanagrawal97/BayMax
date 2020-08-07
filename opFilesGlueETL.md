AWS Glue is based on Apache Spark, which partitions data across multiple nodes to achieve high throughput. When writing data to a file-based sink like Amazon S3, Glue will write a separate file for each partition. In some cases, it may be desirable to change the number of partitions, either to change the degree of parallelism or the number of output files.We would like to control the number of output files or output file size of ETL job


Control the number of partitions(number of files) using repartition():

a) Convert the Glue Dynamic frame to Spark dataframe and leverage the repartition() function in Spark.

```
partitioned_dataframe = datasource0.toDF().repartition(2)
```
b) Write the partitioned dataframe to S3 path. 
```
output=partitioned_dataframe.write.format("csv").save("s3://<bucketname>/<prefixpath>/")
```

Control the number of partitions(number of files) using coalesce():

a) Convert the Glue Dynamic frame to Spark dataframe and leverage the coalesce() function in Spark.

```
partitioned_dataframe = datasource0.toDF().coalesce(2)
```
b) Write the partitioned dataframe to S3 path. 

```
output=partitioned_dataframe.write.format("csv").save("s3://<bucketname>/<prefixpath>/")
```

The coalesce method reduces the number of partitions in a Spark DataFrame. coalesce is faster as it minimizes the data movement.

The repartition algorithm does a full data shuffle and equally distributes the data among the partitions. However as full shuffle is happened it’s a little expensive operation. It does not attempt to minimize data movement like the coalesce algorithm. 

### Limit the number of lines written per file by using the spark configuration parameter "spark.sql.files.maxRecordsPerFile"

Spark 2.2 introduces a maxRecordsPerFile option when you write data out. With "spark.sql.files.maxRecordsPerFile" configuration, you can limit the number of records that get written per file in each partition.

Add this property to GLUE ETL job as below.

Step 1: Navigate to the 'Script libraries and job parameters (optional)’ from the glue job console -> Edit job -> Job parameters -> enter key/value pair'
Step 2: Enter following value for:

Key: --conf 
Value: spark.sql.files.maxRecordsPerFile=10000


