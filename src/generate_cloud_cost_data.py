import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker


fake = Faker("en_US")


SUBSCRIPTIONS = [
    ("SUB-PRD-001", "Production Subscription", "IT", "it-owner@example.com"),
    ("SUB-DEV-001", "Development Subscription", "Engineering", "eng-owner@example.com"),
    ("SUB-DATA-001", "Data Platform Subscription", "Data", "data-owner@example.com"),
]

RESOURCE_GROUPS = [
    ("rg-prod-data-platform", "PROD", "Data", "westeurope"),
    ("rg-dev-data-platform", "DEV", "Data", "westeurope"),
    ("rg-prod-app-services", "PROD", "Application", "northeurope"),
    ("rg-dev-analytics", "DEV", "Analytics", "westeurope"),
    ("rg-shared-monitoring", "SHARED", "Platform", "westeurope"),
]

SERVICES = [
    ("VM", "Virtual Machines", "Compute", "Hours"),
    ("STORAGE", "Storage Account", "Storage", "GB-Month"),
    ("ADF", "Azure Data Factory", "Data Integration", "Activity Runs"),
    ("DBR", "Azure Databricks", "Analytics", "DBU"),
    ("SQLDB", "Azure SQL Database", "Database", "vCore-Hours"),
    ("EVENTHUB", "Event Hubs", "Streaming", "Throughput Units"),
    ("LOG", "Log Analytics", "Monitoring", "GB"),
]

METER_BY_SERVICE = {
    "VM": ["D4s v5 VM Hours", "D8s v5 VM Hours", "E8s v5 VM Hours"],
    "STORAGE": ["Hot LRS Data Stored", "Read Operations", "Write Operations"],
    "ADF": ["Pipeline Activity Runs", "Data Movement Hours"],
    "DBR": ["Jobs Compute DBU", "All Purpose Compute DBU"],
    "SQLDB": ["General Purpose vCore Hours", "Storage GB"],
    "EVENTHUB": ["Standard Throughput Unit", "Ingress Events"],
    "LOG": ["Data Ingestion GB", "Data Retention GB"],
}

UNIT_PRICE_RANGE = {
    "VM": (0.08, 1.20),
    "STORAGE": (0.01, 0.15),
    "ADF": (0.001, 0.05),
    "DBR": (0.15, 0.90),
    "SQLDB": (0.10, 1.50),
    "EVENTHUB": (0.02, 0.30),
    "LOG": (0.20, 2.50),
}


def generate_subscriptions() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "subscription_code": code,
                "subscription_name": name,
                "department": department,
                "owner_email": owner_email,
            }
            for code, name, department, owner_email in SUBSCRIPTIONS
        ]
    )


def generate_resource_groups() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "resource_group_name": name,
                "environment": environment,
                "business_unit": business_unit,
                "region": region,
            }
            for name, environment, business_unit, region in RESOURCE_GROUPS
        ]
    )


def generate_services() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "service_code": code,
                "service_name": name,
                "service_category": category,
                "unit": unit,
            }
            for code, name, category, unit in SERVICES
        ]
    )


def generate_usage_records(days: int = 30, records_per_day: int = 300) -> pd.DataFrame:
    rows = []
    now = datetime.now()
    start_date = now - timedelta(days=days)

    usage_id = 1

    for day_offset in range(days):
        usage_day = start_date + timedelta(days=day_offset)

        for _ in range(records_per_day):
            service_id = random.randint(1, len(SERVICES))
            service_code = SERVICES[service_id - 1][0]

            resource_group_id = random.randint(1, len(RESOURCE_GROUPS))
            resource_group = RESOURCE_GROUPS[resource_group_id - 1]

            subscription_id = random.randint(1, len(SUBSCRIPTIONS))

            usage_ts = usage_day.replace(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59),
                microsecond=0,
            )

            usage_quantity = round(random.uniform(1, 500), 4)
            min_price, max_price = UNIT_PRICE_RANGE[service_code]
            unit_price = round(random.uniform(min_price, max_price), 6)
            cost_amount = round(usage_quantity * unit_price, 4)

            resource_name = f"{service_code.lower()}-{fake.word()}-{random.randint(100, 999)}"

            rows.append(
                {
                    "usage_id": usage_id,
                    "usage_date": usage_ts.date(),
                    "usage_ts": usage_ts,
                    "subscription_id": subscription_id,
                    "resource_group_id": resource_group_id,
                    "service_id": service_id,
                    "resource_name": resource_name,
                    "meter_name": random.choice(METER_BY_SERVICE[service_code]),
                    "region": resource_group[3],
                    "usage_quantity": usage_quantity,
                    "unit_price": unit_price,
                    "cost_amount": cost_amount,
                    "currency": "USD",
                    "pricing_model": random.choice(["PAYG", "RESERVED", "SAVINGS_PLAN"]),
                    "environment": resource_group[1],
                    "source_system": "LOCAL_GENERATOR",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )

            usage_id += 1

    return pd.DataFrame(rows)


def main() -> None:
    subscriptions = generate_subscriptions()
    resource_groups = generate_resource_groups()
    services = generate_services()
    usage = generate_usage_records()

    subscriptions.to_csv("data/sample/dim_subscription.csv", index=False)
    resource_groups.to_csv("data/sample/dim_resource_group.csv", index=False)
    services.to_csv("data/sample/dim_service.csv", index=False)
    usage.to_csv("data/sample/fact_cloud_usage.csv", index=False)

    print("Generated files:")
    print("data/sample/dim_subscription.csv")
    print("data/sample/dim_resource_group.csv")
    print("data/sample/dim_service.csv")
    print("data/sample/fact_cloud_usage.csv")
    print(f"Cloud usage row count: {len(usage)}")


if __name__ == "__main__":
    main()