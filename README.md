# Azure FinOps Lakehouse

End-to-end cloud data engineering project for Azure cost and usage analytics.

This project simulates a FinOps-oriented lakehouse platform using:

- PostgreSQL
- Docker
- Python
- Azure Data Factory
- Self-hosted Integration Runtime
- Azure Data Lake Storage Gen2
- Azure Databricks
- PySpark
- Delta Lake
- Power BI

The goal is to build a modern data engineering pipeline that ingests cloud cost and usage data from a local PostgreSQL source system, lands the raw data into ADLS Gen2 Bronze layer, transforms it with Databricks/PySpark into Silver and Gold Delta Lake layers, and serves analytics through a Power BI FinOps dashboard.

---

## Architecture

```mermaid
flowchart LR
    A["Local PostgreSQL<br/>Docker<br/>finopsdb"] --> B["Azure Data Factory<br/>Copy Pipeline"]
    B --> C["ADLS Gen2<br/>Bronze Layer<br/>Raw CSV"]
    C --> D["Azure Databricks<br/>PySpark"]
    D --> E["ADLS Gen2<br/>Silver Layer<br/>Cleaned Delta"]
    E --> F["Azure Databricks<br/>Gold Mart Aggregations"]
    F --> G["ADLS Gen2<br/>Gold Layer<br/>FinOps Delta Marts"]
    G --> H["Power BI<br/>FinOps Dashboard"]

    I["Self-hosted Integration Runtime"] --> B
    I --> A
