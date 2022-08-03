# Data processing
The processing was as following figure shown.
![Solution design](https://github.com/LeoLee-Xiaohu/IMBA-AWS/blob/aws-v1/imgs/solution_design_aws3.0_pipeline.png)

# 1. Extract data to s3

Create s3 bucket, upload the Raw Data of IMBA.

# 2. Using Glue Crawler to scan the raw data and useing Athena to do auditing 

Scan raw data and create catalog. 
Check the data quality of raw data from the aspects of integrity, consistency and accuracy. For example, checking the null value, totoal number of records, data type, coding format, and so on. 


# 3. Using EventBridge, Lambda, Glue job to do ETL 

EventBridge schedule datapipeline, here, run data pipeline per 30 days.

In the project of IMBA, following features transformations were completed by Glue Job. Please see GLue Job codes in scripts/glue_job.

## step 1. create features - order_product_prior 

This step outputs table "order_product_prior", parquet files.

## step 2. create 4 features - user features, up features, product features   

This step outputs 4 table, parquet files.

# 4. Get final csv data

Glue version: 
``` 
Spark 3.1 python3 (glue version 3.0 )
``` 
Glue Job python code is in the folder named 'scripts'. Please see the file create_results(csv).py.

The following picture shows a part of the reasult data.
![output](https://github.com/LeoLee-Xiaohu/IMBA-AWS/blob/aws-v0/imgs/reasults.png)
