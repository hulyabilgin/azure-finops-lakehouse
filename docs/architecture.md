# Azure FinOps Lakehouse Architecture

## Target Architecture

PostgreSQL Source  
→ Azure Data Factory  
→ ADLS Gen2 Bronze Layer  
→ Azure Databricks / PySpark  
→ Delta Lake Silver & Gold Layers  
→ Power BI FinOps Dashboard

## ADLS Gen2 Layout

```text
finops-lake/
├── bronze/
│   └── cloud_usage/
├── silver/
│   └── cloud_usage_cleaned/
├── gold/
│   ├── finops_daily_cost/
│   ├── finops_service_cost/
│   └── finops_environment_cost/
└── checkpoint/
    └── cloud_usage/