# Databricks Silver to Gold Transformation

## Objective

This step creates business-ready FinOps analytics marts from the cleaned Silver Delta dataset using Azure Databricks and PySpark.

The Gold layer is designed for reporting and dashboarding use cases such as Power BI cost analysis.

## Source

| Setting | Value |
|---|---|
| Source layer | Silver |
| Format | Delta Lake |
| Path | `finops-lake/silver/cloud_usage_cleaned/` |
| Input dataset | Cleaned cloud usage records |

## Target

| Gold Mart | Path | Purpose |
|---|---|---|
| `finops_daily_cost` | `finops-lake/gold/finops_daily_cost/` | Daily cloud cost trend |
| `finops_service_cost` | `finops-lake/gold/finops_service_cost/` | Cost by Azure service |
| `finops_environment_cost` | `finops-lake/gold/finops_environment_cost/` | Cost by environment |
| `finops_top_resources` | `finops-lake/gold/finops_top_resources/` | Top expensive cloud resources |
| `finops_pricing_model_cost` | `finops-lake/gold/finops_pricing_model_cost/` | PAYG vs Reserved vs Savings Plan cost distribution |

## Main Notebook

| Notebook | Purpose |
|---|---|
| `02_silver_to_gold_finops_marts` | Creates Gold FinOps marts from the Silver Delta dataset |

## Transformation Logic

The Databricks notebook performs the following operations:

- Reads the Silver Delta dataset from ADLS Gen2.
- Enriches cloud usage records with service metadata.
- Aggregates daily cloud cost.
- Aggregates cost by service and service category.
- Aggregates cost by environment.
- Calculates top expensive resources.
- Calculates cost distribution by pricing model.
- Adds `gold_processed_at` audit timestamps.
- Writes all Gold marts into ADLS Gen2 in Delta Lake format.

## Gold Mart Details

### 1. `finops_daily_cost`

Daily cloud cost trend.

Main columns:

- `usage_date`
- `total_cost_usd`
- `total_usage_quantity`
- `usage_record_count`
- `distinct_resource_count`
- `avg_record_cost_usd`
- `gold_processed_at`

### 2. `finops_service_cost`

Cloud cost by Azure service.

Main columns:

- `service_id`
- `service_code`
- `service_name`
- `service_category`
- `unit`
- `total_cost_usd`
- `total_usage_quantity`
- `usage_record_count`
- `distinct_resource_count`
- `avg_record_cost_usd`
- `gold_processed_at`

### 3. `finops_environment_cost`

Cloud cost by environment.

Main columns:

- `environment`
- `total_cost_usd`
- `total_usage_quantity`
- `usage_record_count`
- `distinct_resource_count`
- `cost_percentage`
- `gold_processed_at`

### 4. `finops_top_resources`

Top expensive cloud resources.

Main columns:

- `resource_name`
- `environment`
- `region`
- `service_code`
- `service_name`
- `service_category`
- `total_cost_usd`
- `total_usage_quantity`
- `usage_record_count`
- `gold_processed_at`

### 5. `finops_pricing_model_cost`

Cost distribution by pricing model.

Main columns:

- `pricing_model`
- `total_cost_usd`
- `total_usage_quantity`
- `usage_record_count`
- `distinct_resource_count`
- `cost_percentage`
- `gold_processed_at`

## Validation

Expected output counts:

```text
finops_daily_cost: approximately 30 rows
finops_service_cost: 7 rows
finops_environment_cost: 3 rows
finops_top_resources: 50 rows
finops_pricing_model_cost: 3 rows