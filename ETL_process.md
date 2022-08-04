# Data processing
The processing was as following figure shown.
<img src=https://github.com/LeoLee-Xiaohu/IMBA-AWS/blob/aws-v3/imgs/solution_design_aws2.0.drawio.png  width = 80% />

# 1. Extract data to s3

Create s3 bucket, upload the Raw Data of IMBA.

# 2. Using Glue Crawler to scan the raw data and useing Athena to do auditing 

Scan raw data and create catalog. 
Check the data quality of raw data from the aspects of integrity, consistency and accuracy. For example, checking the null value, totoal number of records, data type, coding format, and so on. 


# 3. Using EventBridge, Lambda, Glue job to schedule and do ETL 

EventBridge schedule datapipeline, here, run data pipeline per day UTC23:35.
<div align="center">
<img src=https://github.com/LeoLee-Xiaohu/IMBA-AWS/blob/aws-v3/imgs/eventbridge_scheduler.png width=40% />
</div>
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

# 5. Check whether run successfully automatically
As the we set UTC23:35, the data pipeline will run automatically, from extracting raw data to transformation to generated the final data. 
Firstly, after the data was pull into S3 bucket, the Glue Crawler would scan the raw data folder regularly, such as scanning per day here. 
Then, at UTC23:35, EventBridge trigger lambda and start to run pipelin automatically.

From the glue job monitor, we could know when and how the jobs was run.
In the experiment, we can see the first job started from Sydney time 9:35, which is UTC23:35, and the last job end at Sydney time 10:08.
<div align="center">
<img src=https://github.com/LeoLee-Xiaohu/IMBA-AWS/blob/aws-v3/imgs/jobMonitor.png width=40% />
</div>

We can also see the results data in the s3 bucket was generated successfully.
The following picture shows a part of the reasult data.
![output](https://github.com/LeoLee-Xiaohu/IMBA-AWS/blob/aws-v0/imgs/reasults.png)
