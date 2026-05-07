# Databricks notebook source
storage_account_name = "..."
storage_account_key = "...."
container_name = "finops-lake"

spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
    storage_account_key
)

bronze_path = (
    f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/"
    "bronze/cloud_usage/fact_cloud_usage/fact_cloud_usage.csv"
)

silver_path = (
    f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/"
    "silver/cloud_usage_cleaned/"
)

print(bronze_path)
print(silver_path)

# COMMAND ----------

df_bronze = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "false")
    .csv(bronze_path)
)

display(df_bronze.limit(10))

# COMMAND ----------

df_bronze.count()

# COMMAND ----------

from pyspark.sql.functions import col, to_date, to_timestamp, current_timestamp

df_silver = (
    df_bronze
    .withColumn("usage_id", col("usage_id").cast("long"))
    .withColumn("usage_date", to_date(col("usage_date")))
    .withColumn("usage_ts", to_timestamp(col("usage_ts")))
    .withColumn("subscription_id", col("subscription_id").cast("int"))
    .withColumn("resource_group_id", col("resource_group_id").cast("int"))
    .withColumn("service_id", col("service_id").cast("int"))
    .withColumn("usage_quantity", col("usage_quantity").cast("decimal(18,4)"))
    .withColumn("unit_price", col("unit_price").cast("decimal(18,6)"))
    .withColumn("cost_amount", col("cost_amount").cast("decimal(18,4)"))
    .withColumn("created_at", to_timestamp(col("created_at")))
    .withColumn("updated_at", to_timestamp(col("updated_at")))
    .withColumn("silver_processed_at", current_timestamp())
    .dropDuplicates(["usage_id"])
    .filter(col("usage_id").isNotNull())
    .filter(col("cost_amount") >= 0)
)

display(df_silver.limit(10))

# COMMAND ----------

df_silver.printSchema()
df_silver.count()

# COMMAND ----------

(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(silver_path)
)

print(f"Silver data written to: {silver_path}")

# COMMAND ----------

df_check = spark.read.format("delta").load(silver_path)

display(df_check.limit(10))
df_check.count()

# COMMAND ----------

from pyspark.sql.functions import sum as spark_sum, round as spark_round

df_check.groupBy("environment") \
    .agg(spark_round(spark_sum("cost_amount"), 2).alias("total_cost_usd")) \
    .orderBy(col("total_cost_usd").desc()) \
    .show()

# COMMAND ----------

from pyspark.sql.functions import col, to_date, to_timestamp, current_timestamp

df_silver = (
    df_bronze
    .withColumn("usage_id", col("usage_id").cast("long"))
    .withColumn("usage_date", to_date(col("usage_date")))
    .withColumn("usage_ts", to_timestamp(col("usage_ts")))
    .withColumn("subscription_id", col("subscription_id").cast("int"))
    .withColumn("resource_group_id", col("resource_group_id").cast("int"))
    .withColumn("service_id", col("service_id").cast("int"))
    .withColumn("usage_quantity", col("usage_quantity").cast("decimal(18,4)"))
    .withColumn("unit_price", col("unit_price").cast("decimal(18,6)"))
    .withColumn("cost_amount", col("cost_amount").cast("decimal(18,4)"))
    .withColumn("created_at", to_timestamp(col("created_at")))
    .withColumn("updated_at", to_timestamp(col("updated_at")))
    .withColumn("silver_processed_at", current_timestamp())
    .dropDuplicates(["usage_id"])
    .filter(col("usage_id").isNotNull())
    .filter(col("cost_amount") >= 0)
)

display(df_silver.limit(10))

# COMMAND ----------

df_silver.printSchema()
df_silver.count()

# COMMAND ----------

(
    df_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(silver_path)
)

print(f"Silver data written to: {silver_path}")

# COMMAND ----------

df_check = spark.read.format("delta").load(silver_path)

display(df_check.limit(10))
df_check.count()

# COMMAND ----------

from pyspark.sql.functions import sum as spark_sum, round as spark_round

df_check.groupBy("environment") \
    .agg(spark_round(spark_sum("cost_amount"), 2).alias("total_cost_usd")) \
    .orderBy(col("total_cost_usd").desc()) \
    .show()