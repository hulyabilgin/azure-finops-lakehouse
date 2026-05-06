# ADF Ingestion: PostgreSQL to ADLS Bronze

## Objective

This step implements the first ingestion pipeline of the Azure FinOps Lakehouse project.

The pipeline copies cloud cost and usage data from a local PostgreSQL source database into the ADLS Gen2 Bronze layer.

## Source

| Setting | Value |
|---|---|
| Source system | Local PostgreSQL running in Docker |
| Database | finopsdb |
| Main table | fact_cloud_usage |
| Linked service | ls_postgres_finops_local |
| Integration runtime | ir-selfhosted-local-dev-001 |

## Sink

| Setting | Value |
|---|---|
| Storage | Azure Data Lake Storage Gen2 |
| Storage account | stfinopslakehly00X |
| Container | finops-lake |
| Layer | Bronze |
| Target path | bronze/cloud_usage/fact_cloud_usage/ |
| Output file | fact_cloud_usage.csv |
| Linked service | ls_adls_finops_lake |

## ADF Objects

| Object Type | Name |
|---|---|
| PostgreSQL linked service | ls_postgres_finops_local |
| ADLS Gen2 linked service | ls_adls_finops_lake |
| PostgreSQL dataset | ds_postgres_fact_cloud_usage |
| ADLS Bronze dataset | ds_adls_bronze_fact_cloud_usage_csv |
| Pipeline | pl_copy_fact_cloud_usage_to_bronze |
| Activity | copy_fact_cloud_usage_to_bronze |

## Pipeline Flow

```text
Local PostgreSQL / fact_cloud_usage
        ↓
Azure Data Factory Copy Activity
        ↓
ADLS Gen2 / finops-lake / bronze / cloud_usage / fact_cloud_usage.csv