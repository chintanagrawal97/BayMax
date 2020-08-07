### convert from dynamic frame to dataframe ====
df1 = dyf1.toDF()
 
### convert from dataframe to dynamicframe ==== 
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
glueContext = GlueContext(sc)
dyf1 = DynamicFrame.fromDF( medicare , glueContext, "nested")
 
 
###  ApplyMapping   =====
applymapping1 = ApplyMapping.apply(frame = dyf1, mappings = [("col1", "string", "newcol1", "string"), ("col2", "string", "newcol2", "string")], transformation_ctx = "applymapping1")
 
applymapping1 = ApplyMapping.apply(frame = df1, mappings = [("col1", "string", "newcol1", "string"), ("col2", "string", "newcol2", "string")], transformation_ctx = "applymapping1")
 
 
 
###  SelectFields ====
selectfields2 = SelectFields.apply(frame = applymapping1, paths = ["newcol1"], transformation_ctx = "selectfields2") 
 
 
###  ResolveChoice ==
resolvechoice3 = ResolveChoice.apply(frame = selectfields2, choice = "MATCH_CATALOG", database = "sampledb", table_name = "test2-1", transformation_ctx = "resolvechoice3")
 
### Write dynamic frame ======
 
datasink4 = glueContext.write_dynamic_frame.from_catalog(frame = datasource0, name_space = "default", table_name = 'leeys', transformation_ctx = "datasink4")
 
 
 
datasink4 = glueContext.write_dynamic_frame.from_options(frame = addpartitionfield, connection_type = "s3", connection_options = {"path": "s3://t1-saas-insights-dev-ap-southeast-2/glue/processed", "partitionKeys": ["date_p"]}, format = "parquet", transformation_ctx = "datasink4")
 
 
response = glueContext.write_dynamic_frame.from_options(frame = sourcedb,
                                                   connection_type = "postgresql" ,
                                                   connection_options = {"url": "jdbc:postgresql://target.c3o7whfeiyfn.us-east-1.rds.amazonaws.com/targetdb", "user": "leeys", "password": "Welcome1!", "dbtable": "public.cities"}
                                                   )
 
response = glueContext.write_dynamic_frame.from_options(frame = sourcedb,
                                                   connection_type = "mysql" ,
                                                   connection_options = {"url": "jdbc:mysql://leeys1.c3o7whfeiyfn.us-east-1.rds.amazonaws.com", "user": "leeys", "password": "welcome1", "dbtable": "leeysdb.csv7"}
                                                   )
 
glueContext.write_dynamic_frame.from_options(frame = l_history,
          connection_type = "s3",
          connection_options = {"path": "s3://leeys-virginia/output-dir/legislator_history"},
          format = "parquet") 
 
 
response = glueContext.write_dynamic_frame.from_jdbc_conf(frame = df_mapped,
                                                   catalog_connection = "red1",
                                                   connection_options = {"dbtable": "public.test1", "database": "leeysdb"},
                                                   redshift_tmp_dir = "s3://leeys-virginia/glue/temp-dir/")
 
 
response = glueContext.write_dynamic_frame.from_jdbc_conf(frame = df_mapped,
                                                   catalog_connection = "red1",
                                                   connection_options = {"dbtable": "public.test1",
                                                                         "database": "leeysdb" ,
                                                                         "preactions":"delete from public.test1;",
                                                                         "extracopyoptions":"MAXERROR 2"},
                                                   redshift_tmp_dir = "s3://leeys-virginia/glue/temp-dir/")
 
datasink4 = glueContext.write_dynamic_frame.from_options(frame = addpartitionfield, connection_type = "s3", connection_options = {"path": "s3://t1-saas-insights-dev-ap-southeast-2/glue/processed", "partitionKeys": ["date_p"]}, format = "parquet", transformation_ctx = "datasink4")
 
 
 
 
#### use  Get sink rather than write_dynamic_frame
data_sink = glueContext.getSink("s3://leeys-virginia/glue/temp/" , format = "json" )
( or data_sink.setFormat("json")  )
data_sink.writeFrame(myFrame)