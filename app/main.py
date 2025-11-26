import sys
from pathlib import Path
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from db.client import client
from infra.redis.client import RedisCache

app = FastAPI(title="Distributed Log Processing System API")
redis = RedisCache()

# -------------------------------
# Models
# -------------------------------

class SuggestFixRequest(BaseModel):
    error: str

class SummarizeLogsRequest(BaseModel):
    logs: List[Dict[str, Any]]
    max_chars: Optional[int] = 400

# -------------------------------
# Helper Functions
# -------------------------------
def build_time_range(time_range: str) -> str:
    if time_range.endswith("m"):
        return f"now('UTC') - INTERVAL {time_range[:-1]} MINUTE"
    if time_range.endswith("h"):
        return f"now('UTC') - INTERVAL {time_range[:-1]} HOUR"
    if time_range.endswith("d"):
        return f"now('UTC') - INTERVAL {time_range[:-1]} DAY"
    return "now('UTC') - INTERVAL 1 HOUR"

def cache(endpoint, params, compute_fn, ttl=60):
    key = redis.get_key(endpoint, params)
    cached = redis.get(key)
    if cached:
        return cached
    value = compute_fn()
    redis.set(key, value, ttl)
    return value

# -------------------------------
# Endpoints
# -------------------------------

@app.get("/get_logs")
def get_logs(
    time_range: str = "1h",
    log_level: Optional[str] = None,
    source_type: Optional[str] = None,
    service_name: Optional[str] = None,
    host_ip: Optional[str] = None,
    message_contains: Optional[str] = None,
    trace_id: Optional[str] = None,
    limit: int = 200,
):
    conditions = [f"timestamp >= {build_time_range(time_range)}"]
    if log_level:
        conditions.append(f"severity = '{log_level}'")
    if source_type:
        conditions.append(f"source_type = '{source_type}'")
    if service_name:
        conditions.append(f"service_name = '{service_name}'")
    if host_ip:
        conditions.append(f"host_ip = '{host_ip}'")
    if message_contains:
        conditions.append(f"message ILIKE '%{message_contains}%'")
    if trace_id:
        conditions.append(f"trace_id = '{trace_id}'")
    where_clause = " AND ".join(conditions)
    query = f"""
        SELECT *
        FROM logs
        WHERE {where_clause}
        ORDER BY timestamp DESC
        LIMIT {limit}
    """
    result = client.query(query).result_rows
    columns = client.query(query).column_names
    return [dict(zip(columns, row)) for row in result]


@app.post("/suggest_fix")
def suggest_fix(payload: SuggestFixRequest):
    error = payload.error
    fake_result = {
        "error": error,
        "likely_cause": "Possible database/network timeout or invalid configuration.",
        "suggested_fix": "Check DB connection pool, retry logic, and service configuration.",
    }
    return fake_result


@app.get("/dashboard/top_errors")
def dashboard_top_errors(time_range: str = "1h", limit: int = 20):
    def compute():
        query = f"""
            SELECT
                message,
                count() AS occurrences,
                groupArrayDistinct(service_name) AS services
            FROM logs
            WHERE severity = 'ERROR'
            AND timestamp >= {build_time_range(time_range)}
            GROUP BY message
            ORDER BY occurrences DESC
            LIMIT {limit}
        """
        rows = client.query(query).result_rows
        columns = client.query(query).column_names
        return [dict(zip(columns, row)) for row in rows]
    return cache("top_errors", {"time_range": time_range, "limit": limit}, compute)


@app.get("/dashboard/top_services")
def dashboard_top_services(time_range: str = "1h"):
    def compute():
        query = f"""
            SELECT
                service_name,
                count() AS logs,
                sum(severity = 'ERROR') AS errors,
                errors / logs AS error_ratio
            FROM logs
            WHERE timestamp >= {build_time_range(time_range)}
            GROUP BY service_name
            ORDER BY logs DESC
        """
        rows = client.query(query).result_rows
        columns = client.query(query).column_names
        return [dict(zip(columns, row)) for row in rows]
    return cache("top_services", {"time_range": time_range}, compute)


@app.get("/dashboard/services")
def dashboard_services(time_range: str = "24h"):
    def compute():
        query = f"""
            SELECT
                service_name,
                max(timestamp) AS last_seen
            FROM logs
            WHERE timestamp >= {build_time_range(time_range)}
            GROUP BY service_name
            ORDER BY last_seen DESC
        """
        rows = client.query(query).result_rows
        columns = client.query(query).column_names
        return [dict(zip(columns, row)) for row in rows]
    return cache("services_list", {"time_range": time_range}, compute)


@app.get("/dashboard/error_heatmap")
def dashboard_error_heatmap(time_range: str = "6h"):
    def compute():
        query = f"""
            SELECT
                service_name,
                severity,
                count() AS count
            FROM logs
            WHERE timestamp >= {build_time_range(time_range)}
            GROUP BY service_name, severity
            ORDER BY service_name, severity
        """
        rows = client.query(query).result_rows
        columns = client.query(query).column_names
        return [dict(zip(columns, row)) for row in rows]
    return cache("error_heatmap", {"time_range": time_range}, compute)
