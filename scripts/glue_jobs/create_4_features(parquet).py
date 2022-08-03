from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SQLContext

def main():

    # create glue context first
    glueContext = GlueContext(SparkContext.getOrCreate())
    spark_session = glueContext.spark_session
    sqlContext = SQLContext(spark_session.sparkContext, spark_session)

    # creating dataframes from athena
    order = glueContext.create_dynamic_frame.from_catalog(database="imba_small", table_name="orders")
    order_product_prior = glueContext.create_dynamic_frame_from_options(connection_type = "parquet", connection_options = {"paths": ["s3://imba-aws/features/order_products_prior/"]})
   
    # convert glue dynamic dataframe to spark dataframe
    od = order.toDF()
    op = order_product_prior.toDF()
    
		#create temp table for SQL 
    od.registerTempTable('orders')
    op.registerTempTable('order_products_prior')
    
    # user_feature_1 
    user_feature_1 = sqlContext.sql("""
    select user_id,
        max(order_number) as max_order_number,
        sum(days_since_prior_order) as totall_days_prior_order,
        avg(days_since_prior_order) as avg_days_priro_order
    from orders 
    group by user_id
    """)

    # user_feature_2
    user_feature_2 = sqlContext.sql("""
    SELECT user_id,
        Count(*) AS user_total_products,
        Count(DISTINCT product_id) AS user_distinct_products ,
        Sum(CASE WHEN reordered = 1 THEN 1 ELSE 0 END) / Cast(Sum(CASE WHEN order_number > 1 THEN 1 ELSE 0 END) AS DOUBLE)AS user_reorder_ratio
    FROM order_products_prior GROUP BY user_id
    """)   
    
    # up_features
    up_features = sqlContext.sql("""
    SELECT user_id, 
        product_id,
        Count(*) AS up_orders,
        Min(order_number) AS up_first_order, 
        Max(order_number) AS up_last_order, 
        Avg(add_to_cart_order) AS up_average_cart_position
    FROM order_products_prior GROUP BY user_id,
    product_id
    """)

    #prd-feaures 
    prd_feaures = sqlContext.sql("""
    select 
        product_id,
        Count(*) AS prod_orders,
        Sum(reordered) AS prod_reorders,
        Sum(CASE WHEN product_seq_time = 1 THEN 1 ELSE 0 END) AS prod_first_orders,
        Sum(CASE WHEN product_seq_time = 2 THEN 1 ELSE 0 END) AS prod_second_orders
    from 
        (select * , 
            rank() over (partition by user_id , product_id order by order_number ) as product_seq_time 
        from order_products_prior ) a
    group by product_id
    """)


    # save as parquet
    user_feature_1.write.mode('overwrite').format('parquet').save("s3://imba-aws/features/user_features_1_db", header = 'true')
    user_feature_2.write.mode('overwrite').format('parquet').save("s3://imba-aws/features/user_features_2_db", header = 'true')
    up_features.write.mode('overwrite').format('parquet').save("s3://imba-aws/features/up_features_db", header = 'true')
    prd_feaures.write.mode('overwrite').format('parquet').save("s3://imba-aws/features/prd_features_db", header = 'true')
    


if __name__ == '__main__':
    main()