from pathlib import Path

import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "finopsdb",
    "user": "finops_user",
    "password": "finops_pass",
}


def copy_csv_to_table(cursor, table_name: str, csv_path: str, columns: list[str]) -> None:
    columns_sql = ", ".join(columns)

    with open(csv_path, "r", encoding="utf-8") as file:
        next(file)
        cursor.copy_expert(
            f"""
            COPY {table_name} ({columns_sql})
            FROM STDIN
            WITH CSV
            """,
            file,
        )


def main() -> None:
    base_path = Path("data/sample")

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        cursor.execute("TRUNCATE fact_cloud_usage RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE dim_subscription RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE dim_resource_group RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE dim_service RESTART IDENTITY CASCADE;")

        copy_csv_to_table(
            cursor,
            "dim_subscription",
            str(base_path / "dim_subscription.csv"),
            ["subscription_code", "subscription_name", "department", "owner_email"],
        )

        copy_csv_to_table(
            cursor,
            "dim_resource_group",
            str(base_path / "dim_resource_group.csv"),
            ["resource_group_name", "environment", "business_unit", "region"],
        )

        copy_csv_to_table(
            cursor,
            "dim_service",
            str(base_path / "dim_service.csv"),
            ["service_code", "service_name", "service_category", "unit"],
        )

        copy_csv_to_table(
            cursor,
            "fact_cloud_usage",
            str(base_path / "fact_cloud_usage.csv"),
            [
                "usage_id",
                "usage_date",
                "usage_ts",
                "subscription_id",
                "resource_group_id",
                "service_id",
                "resource_name",
                "meter_name",
                "region",
                "usage_quantity",
                "unit_price",
                "cost_amount",
                "currency",
                "pricing_model",
                "environment",
                "source_system",
                "created_at",
                "updated_at",
            ],
        )

        cursor.execute(
            """
            INSERT INTO etl_watermark (pipeline_name, last_loaded_at)
            VALUES ('postgres_cloud_usage_to_adls_bronze', '1900-01-01')
            ON CONFLICT (pipeline_name)
            DO UPDATE SET last_loaded_at = EXCLUDED.last_loaded_at,
                          updated_at = CURRENT_TIMESTAMP;
            """
        )

        conn.commit()
        print("Cloud cost data loaded successfully.")

    except Exception as exc:
        conn.rollback()
        raise exc

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()