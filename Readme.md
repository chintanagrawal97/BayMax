 ### BayMax

I have seen on many ocassion ETL developer struggling with loading or reading their datasets from different databases in AWS Glue. The intricacies of each database are often very differnet and a solution provided for PostGres would not not work for Oracle Database. Engineers might not be experienced with all the favours of Dtabases and can often face challenges with simple steps such as setting up schema , creating table , loading data etc. Often engineers can be found struggling with setting up Glue Connection to their DevEndpoint and reading and writing datasets which are the prerequisite to for testing. This script shall automate the provisioning of Glue DevEndpoint , RDS Databases and connect them using Glue Connection. It shall ebnable engineer to get started quickly and focus more on their use case.

It helps you provision the most effective environment 

The setup can often be overwhelming for engineers who are new to AWS or Software Developers who have had less experience with Spark and Glue API .

Often Engineers leave their devendpoints/databases running as they feel they might face difficulties setting up replication environment again. This incurrs a lot of charges to the company which can be easily avoided. 

After doing the required testing you can terminate the resources using cleanup script.