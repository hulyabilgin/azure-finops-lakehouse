# Databricks Bronze to Silver Transformation

## Objective

This step transforms raw cloud cost and usage data from the ADLS Gen2 Bronze layer into a cleaned Silver layer using Azure Databricks and PySpark.

## Source

| Setting | Value |
|---|---|
| Source layer | Bronze |
| Format | CSV |
| Path | finops-lake/bronze/cloud_usage/fact_cloud_usage/fact_cloud_usage.csv |

## Target

| Setting | Value |
|---|---|
| Target layer | Silver |
| Format | Delta Lake |
| Path | finops-lake/silver/cloud_usage_cleaned/ |

## Transformation Logic

The Databricks notebook performs the following operations:

- Reads the raw Bronze CSV file from ADLS Gen2.
- Casts string-based CSV columns into proper data types.
- Converts date and timestamp columns.
- Converts numeric cost and usage columns into decimal types.
- Removes duplicate records based on `usage_id`.
- Filters invalid records where `usage_id` is null.
- Filters records where `cost_amount` is negative.
- Adds a `silver_processed_at` audit column.
- Writes the cleaned dataset into the Silver layer in Delta format.

## Main Notebook

| Notebook | Purpose |
|---|---|
| `01_bronze_to_silver_cloud_usage` | Cleans Bronze cloud usage data and writes Silver Delta output |

## Validation

Expected row count:

```text
Bronze row count: 9000
Silver row count: 9000