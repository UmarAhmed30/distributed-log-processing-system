CREATE TABLE logs (
    log_id UUID,
    timestamp DateTime64(3, 'UTC'),
    severity LowCardinality(String),
    source_type LowCardinality(String),
    service_name LowCardinality(String),
    host String,
    host_ip IPv4,
    file_path String,
    message String,
    raw_message String,
    trace_id String,
    span_id String,
    metadata String
)
ENGINE = ReplacingMergeTree
ORDER BY timestamp
TTL toDateTime(timestamp) + INTERVAL 30 DAY

SELECT count() FROM logs;

INSERT INTO logs (
    timestamp,
    severity,
    source_type,
    service_name,
    host,
    host_ip,
    file_path,
    message,
    raw_message,
    trace_id,
    span_id,
    metadata
) VALUES (
    '2025-11-23 18:45:12.500',
    'ERROR',
    'server',
    'nginx',
    'gcp-vm-3',
    '10.128.0.42',
    '/var/log/payment-service/app.log',
    'Nginx failed to reach backend',
    'GET /api/v1/user 502 120ms upstream error',
    'trace-89123',
    'span-backend',
    '{"method":"GET","path":"/api/v1/user","status_code":502,"latency_ms":120,"upstream":"backend-service"}'
);

SELECT * FROM logs LIMIT 10;

ALTER TABLE logs MODIFY COLUMN log_id UUID default generateUUIDv4();