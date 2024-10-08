import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1728258504961 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://etl-data-engineering-project/output/"], "recurse": True}, transformation_ctx="AmazonS3_node1728258504961")


# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=AmazonS3_node1728258504961,
    mappings=[
        ("new_year", "string", "year", "string"),
        ("cnt", "long", "noofcustomer", "BIGINT"),
        ("qty", "long", "quantity", "BIGINT"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node Amazon Redshift
AmazonRedshift_node1728258509673 = glueContext.write_dynamic_frame.from_options(frame=ApplyMapping_node2, connection_type="redshift", connection_options={"redshiftTmpDir": "s3://etl-data-engineering-project/temp/", "useConnectionProperties": "true", "dbtable": "public.product_tab_def", "connectionName": "MyRedshiftConnection", "preactions": "CREATE TABLE IF NOT EXISTS public.product_tab_def (new_year VARCHAR, noofcustomer BIGINT, quantity BIGINT);"}, transformation_ctx="AmazonRedshift_node1728258509673")

job.commit()
