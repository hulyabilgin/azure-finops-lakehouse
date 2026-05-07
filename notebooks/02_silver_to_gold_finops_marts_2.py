# Databricks notebook source
storage_account_name = "..."
storage_account_key = "...."
container_name = "finops-lake"

spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
    storage_account_key
)

base_path = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net"

gold_tables = {
    "finops_daily_cost": f"{base_path}/gold/finops_daily_cost/",
    "finops_service_cost": f"{base_path}/gold/finops_service_cost/",
    "finops_environment_cost": f"{base_path}/gold/finops_environment_cost/",
    "finops_top_resources": f"{base_path}/gold/finops_top_resources/",
    "finops_pricing_model_cost": f"{base_path}/gold/finops_pricing_model_cost/",
}

export_base_path = f"{base_path}/powerbi_exports"


def export_delta_to_single_csv(table_name: str, delta_path: str) -> None:
    temp_path = f"{export_base_path}/_tmp_{table_name}"
    final_path = f"{export_base_path}/{table_name}.csv"

    df = spark.read.format("delta").load(delta_path)

    (
        df.coalesce(1)
        .write
        .mode("overwrite")
        .option("header", "true")
        .csv(temp_path)
    )

    files = dbutils.fs.ls(temp_path)
    csv_file = [f.path for f in files if f.name.startswith("part-") and f.name.endswith(".csv")][0]

    try:
        dbutils.fs.rm(final_path)
    except Exception:
        pass

    dbutils.fs.mv(csv_file, final_path)
    dbutils.fs.rm(temp_path, recurse=True)

    print(f"Exported {table_name} to {final_path}")


for table_name, delta_path in gold_tables.items():
    export_delta_to_single_csv(table_name, delta_path)