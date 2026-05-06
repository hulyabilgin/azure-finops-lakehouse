# Cost Control

This project uses a small Azure development environment for learning and portfolio purposes.

## Budget

A monthly Azure budget is configured to monitor project costs.

| Setting | Value |
|---|---|
| Budget name | budget-finops-lakehouse-dev-001 |
| Scope | rg-finops-lakehouse-dev-we-001 |
| Reset period | Monthly |
| Budget amount | 5 USD |
| Alerts | 50%, 80%, 100% actual cost |

## Azure Resources Created So Far

| Resource Type | Name |
|---|---|
| Resource Group | rg-finops-lakehouse-dev-we-001 |
| Storage Account | stfinopslakehly001 |
| Container | finops-lake |
| Hierarchical namespace | Enabled |

## Cost-Sensitive Resources

The most cost-sensitive resources in this project are:

- Azure Databricks clusters
- Azure Data Factory pipeline runs
- Storage transactions and capacity
- Log Analytics, if enabled later

## Cost Control Practices

- Use LRS storage for development.
- Keep datasets small.
- Stop Databricks clusters after use.
- Configure Databricks auto-termination.
- Avoid unnecessary always-on compute.
- Delete unused resources after testing.