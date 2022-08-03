import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job



def main():

    # create glue context first
    glueContext = GlueContext(SparkContext.getOrCreate())
    
    
    # creating dataframes from existing athena catelog
    up_features = glueContext.create_dynamic_frame_from_options(connection_type = "parquet", connection_options = {"paths": ["s3://imba-aws/features/up_feature_db/"]})
    prd_features = glueContext.create_dynamic_frame_from_options(connection_type = "parquet", connection_options = {"paths": ["s3://imba-aws/features/prd_feature_db/"]})
    user_features_1 = glueContext.create_dynamic_frame_from_options(connection_type = "parquet", connection_options = {"paths": ["s3://imba-aws/features/user_features_1_db/"]})
    user_features_2 = glueContext.create_dynamic_frame_from_options(connection_type = "parquet", connection_options = {"paths": ["s3://imba-aws/features/user_features_2_db/"]})
    
    # join user features together
    users = Join.apply(user_features_1.rename_field('user_id','user_id1'), user_features_2, 'user_id1', 'user_id').drop_fields(['user_id1'])
    
    # join everything together
    df = Join.apply(Join.apply(up_features, 
                      users.rename_field('user_id','user_id1'), 
                      'user_id','user_id1').drop_fields(['user_id1']),
          prd_features.rename_field('product_id','product_id1'), 
          'product_id','product_id1').drop_fields(['product_id1'])
          
    # convert glue dynamic dataframe to spark dataframe
    df_spark = df.toDF()
    
    # define schema
    schema = StructType() \
      .add("product_id",IntegerType(),False) \
      .add("up_orders",IntegerType(),True) \
      .add("avg_days_prior_order",DoubleType(),True) \
      .add("totall_days_prior_order",DoubleType(),True) \
      .add("user_distinct_products",IntegerType(),True) \
      .add("prod_second_orders",IntegerType(),True) \
      .add("prod_reorders",IntegerType(),True) \
      .add("user_reorder_ratio",DoubleType(),True) \
      .add("user_total_products",IntegerType(),True) \
      .add("up_average_cart_position",DoubleType(),True) \
      .add("up_first_order",IntegerType(),True) \
      .add("max_order_number",IntegerType(),True) \
      .add("prod_orders",IntegerType(),True) \
      .add("up_last_order",IntegerType(),True) \
      .add("prod_first_orders",IntegerType(),True) \
      .add("user_id",IntegerType(),False) 

    # save csv
    df_spark.schema(schema).repartition(1).write.mode('overwrite').format('csv').save("s3://imba-aws/output", header = 'true')
    
if __name__ == '__main__':
    main()
