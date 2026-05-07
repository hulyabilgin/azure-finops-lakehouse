# Power BI FinOps Dashboard Report

## Report Name

**Azure FinOps Lakehouse – Cost Overview Dashboard**

## Objective

This Power BI report visualizes cloud cost and usage analytics generated from the Azure FinOps Lakehouse project.

The dashboard is designed to help analyze:

- Total cloud cost
- Daily cost trend
- Cost by Azure service
- Cost by environment
- Top expensive cloud resources
- PAYG vs Reserved vs Savings Plan distribution

## Data Source

The report uses Gold layer datasets produced by Azure Databricks and stored in ADLS Gen2.

```text
ADLS Gen2 / finops-lake / gold
├── finops_daily_cost
├── finops_service_cost
├── finops_environment_cost
├── finops_top_resources
└── finops_pricing_model_cost