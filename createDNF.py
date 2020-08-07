    #### Create dynamic frame =====
    datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "sampledb", table_name = "glue1", transformation_ctx = "datasource0")
     
     
    applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("timestamp", "string", "storecd", "string"), ("timestamp2", "string", "timestamp2", "string"), ("random_num", "string", "random_num", "string"), ("loglevel", "string", "mcode_cd", "string"), ("junk", "string", "custcnt", "int"), ("message", "string", "occdate", "string")], transformation_ctx = "applymapping1")
     
     
    dyf1 = glueContext.create_dynamic_frame.from_catalog ( database = "sampledb", table_name="csv1" , transformation_ctx= "dfy1" )
    dyf1.show()
     
    datasource0 = glueContext.create_dynamic_frame_from_options("s3", {'paths': ["s3://henry-virginia/glue/csv/"],"recurse": True  }, format="csv")
     
     
    datasource1 = glueContext.create_dynamic_frame_from_options("s3", {'paths': ["s3://henry-virginia/glue/csv2/"],"recurse": True  }, format="csv" , format_options={"skipFirst": True , "withHeader": True , "separator":"\t"  }  )
     
    datasource2 = glueContext.create_dynamic_frame.from_catalog ( database = "sampledb", table_name="csv2" , transformation_ctx= "datasource2" )
     
     
    datasource1 = glueContext.create_dynamic_frame_from_options("s3", {'paths': ["s3://henry-virginia/glue/csv2/"],"recurse": True  }, format="csv" , format_options={"skipFirst": True , "withHeader": True , "separator":"\t"  }  )