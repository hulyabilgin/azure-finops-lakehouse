DROP TABLE IF EXISTS fact_cloud_usage CASCADE;
DROP TABLE IF EXISTS dim_service CASCADE;
DROP TABLE IF EXISTS dim_resource_group CASCADE;
DROP TABLE IF EXISTS dim_subscription CASCADE;
DROP TABLE IF EXISTS etl_watermark CASCADE;

CREATE TABLE dim_subscription (
    subscription_id SERIAL PRIMARY KEY,
    subscription_code VARCHAR(50) NOT NULL UNIQUE,
    subscription_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    owner_email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_resource_group (
    resource_group_id SERIAL PRIMARY KEY,
    resource_group_name VARCHAR(100) NOT NULL UNIQUE,
    environment VARCHAR(30) NOT NULL,
    business_unit VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_service (
    service_id SERIAL PRIMARY KEY,
    service_code VARCHAR(50) NOT NULL UNIQUE,
    service_name VARCHAR(100) NOT NULL,
    service_category VARCHAR(50) NOT NULL,
    unit VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_cloud_usage (
    usage_id BIGSERIAL PRIMARY KEY,
    usage_date DATE NOT NULL,
    usage_ts TIMESTAMP NOT NULL,

    subscription_id INT NOT NULL REFERENCES dim_subscription(subscription_id),
    resource_group_id INT NOT NULL REFERENCES dim_resource_group(resource_group_id),
    service_id INT NOT NULL REFERENCES dim_service(service_id),

    resource_name VARCHAR(150) NOT NULL,
    meter_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,

    usage_quantity NUMERIC(18, 4) NOT NULL,
    unit_price NUMERIC(18, 6) NOT NULL,
    cost_amount NUMERIC(18, 4) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',

    pricing_model VARCHAR(30) NOT NULL,
    environment VARCHAR(30) NOT NULL,

    source_system VARCHAR(50) DEFAULT 'LOCAL_POSTGRES',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE etl_watermark (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    last_loaded_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);