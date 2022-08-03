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
    order_product = glueContext.create_dynamic_frame.from_catalog(database="imba_small", table_name="order_products")
   
    # convert glue dynamic dataframe to spark dataframe
    od = order.toDF()
    op = order_product.toDF()
    
		#create temp table for SQL 
    od.registerTempTable('orders')
    op.registerTempTable('order_products')
    
    # join 2 tables together
    prior = sqlContext.sql("""
    select a.*, 
    b.product_id,
    b.add_to_cart_order,
    b.reordered
    from orders a join order_products b on a.order_id = b.order_id
    where a.eval_set = 'prior'
    """)
          
    
    # save as parquet
    prior.write.mode('overwrite').format('parquet').save("s3://imba-aws/features/order_products_prior", header = 'true')
    
if __name__ == '__main__':
    main()