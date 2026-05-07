# Databricks notebook source
storage_account_name = "..."
storage_account_key = "...."
# Databricks notebook source
container_name = "finops-lake"

spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
    storage_account_key
)

base_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"

silver_path = f"{base_path}/silver/cloud_usage_cleaned/"

gold_daily_cost_path = f"{base_path}/gold/finops_daily_cost/"
gold_service_cost_path = f"{base_path}/gold/finops_service_cost/"
gold_environment_cost_path = f"{base_path}/gold/finops_environment_cost/"
gold_top_resources_path = f"{base_path}/gold/finops_top_resources/"
gold_pricing_model_cost_path = f"{base_path}/gold/finops_pricing_model_cost/"

print("Silver path:", silver_path)
print("Gold daily cost path:", gold_daily_cost_path)

# COMMAND ----------

df_silver = spark.read.format("delta").load(silver_path)

display(df_silver.limit(10))

silver_count = df_silver.count()
print(f"Silver row count: {silver_count}")

# COMMAND ----------

service_rows = [
    (1, "VM", "Virtual Machines", "Compute", "Hours"),
    (2, "STORAGE", "Storage Account", "Storage", "GB-Month"),
    (3, "ADF", "Azure Data Factory", "Data Integration", "Activity Runs"),
    (4, "DBR", "Azure Databricks", "Analytics", "DBU"),
    (5, "SQLDB", "Azure SQL Database", "Database", "vCore-Hours"),
    (6, "EVENTHUB", "Event Hubs", "Streaming", "Throughput Units"),
    (7, "LOG", "Log Analytics", "Monitoring", "GB"),
]

service_columns = [
    "service_id",
    "service_code",
    "service_name",
    "service_category",
    "unit"
]

df_service = spark.createDataFrame(service_rows, service_columns)

df_gold_base = (
    df_silver
    .join(df_service, on="service_id", how="left")
)

display(df_gold_base.limit(10))

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    count,
    countDistinct,
    sum as spark_sum,
    avg,
    round as spark_round,
    current_timestamp
)

df_gold_daily_cost = (
    df_gold_base
    .groupBy("usage_date")
    .agg(
        spark_round(spark_sum("cost_amount"), 2).alias("total_cost_usd"),
        spark_round(spark_sum("usage_quantity"), 2).alias("total_usage_quantity"),
        count("*").alias("usage_record_count"),
        countDistinct("resource_name").alias("distinct_resource_count"),
        spark_round(avg("cost_amount"), 2).alias("avg_record_cost_usd")
    )
    .withColumn("gold_processed_at", current_timestamp())
    .orderBy("usage_date")
)

display(df_gold_daily_cost)

# COMMAND ----------

df_gold_service_cost = (
    df_gold_base
    .groupBy(
        "service_id",
        "service_code",
        "service_name",
        "service_category",
        "unit"
    )
    .agg(
        spark_round(spark_sum("cost_amount"), 2).alias("total_cost_usd"),
        spark_round(spark_sum("usage_quantity"), 2).alias("total_usage_quantity"),
        count("*").alias("usage_record_count"),
        countDistinct("resource_name").alias("distinct_resource_count"),
        spark_round(avg("cost_amount"), 2).alias("avg_record_cost_usd")
    )
    .withColumn("gold_processed_at", current_timestamp())
    .orderBy(col("total_cost_usd").desc())
)

display(df_gold_service_cost)

# COMMAND ----------

total_cost = df_gold_base.agg(spark_sum("cost_amount").alias("total_cost")).collect()[0]["total_cost"]

df_gold_environment_cost = (
    df_gold_base
    .groupBy("environment")
    .agg(
        spark_round(spark_sum("cost_amount"), 2).alias("total_cost_usd"),
        spark_round(spark_sum("usage_quantity"), 2).alias("total_usage_quantity"),
        count("*").alias("usage_record_count"),
        countDistinct("resource_name").alias("distinct_resource_count")
    )
    .withColumn(
        "cost_percentage",
        spark_round((col("total_cost_usd") / float(total_cost)) * 100, 2)
    )
    .withColumn("gold_processed_at", current_timestamp())
    .orderBy(col("total_cost_usd").desc())
)

display(df_gold_environment_cost)

# COMMAND ----------

df_gold_top_resources = (
    df_gold_base
    .groupBy(
        "resource_name",
        "environment",
        "region",
        "service_code",
        "service_name",
        "service_category"
    )
    .agg(
        spark_round(spark_sum("cost_amount"), 2).alias("total_cost_usd"),
        spark_round(spark_sum("usage_quantity"), 2).alias("total_usage_quantity"),
        count("*").alias("usage_record_count")
    )
    .withColumn("gold_processed_at", current_timestamp())
    .orderBy(col("total_cost_usd").desc())
    .limit(50)
)

display(df_gold_top_resources)

# COMMAND ----------

df_gold_pricing_model_cost = (
    df_gold_base
    .groupBy("pricing_model")
    .agg(
        spark_round(spark_sum("cost_amount"), 2).alias("total_cost_usd"),
        spark_round(spark_sum("usage_quantity"), 2).alias("total_usage_quantity"),
        count("*").alias("usage_record_count"),
        countDistinct("resource_name").alias("distinct_resource_count")
    )
    .withColumn(
        "cost_percentage",
        spark_round((col("total_cost_usd") / float(total_cost)) * 100, 2)
    )
    .withColumn("gold_processed_at", current_timestamp())
    .orderBy(col("total_cost_usd").desc())
)

display(df_gold_pricing_model_cost)

# COMMAND ----------

def write_delta(df, path: str) -> None:
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(path)
    )
    print(f"Written: {path}")


write_delta(df_gold_daily_cost, gold_daily_cost_path)
write_delta(df_gold_service_cost, gold_service_cost_path)
write_delta(df_gold_environment_cost, gold_environment_cost_path)
write_delta(df_gold_top_resources, gold_top_resources_path)
write_delta(df_gold_pricing_model_cost, gold_pricing_model_cost_path)

# COMMAND ----------

gold_tables = {
    "finops_daily_cost": gold_daily_cost_path,
    "finops_service_cost": gold_service_cost_path,
    "finops_environment_cost": gold_environment_cost_path,
    "finops_top_resources": gold_top_resources_path,
    "finops_pricing_model_cost": gold_pricing_model_cost_path,
}

for table_name, path in gold_tables.items():
    df = spark.read.format("delta").load(path)
    print(f"{table_name}: {df.count()} rows")