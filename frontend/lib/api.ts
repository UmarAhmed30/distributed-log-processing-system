import axios from 'axios';

// API base URL - points to your FastAPI backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// TypeScript interfaces for your API responses
export interface LogEntry {
  log_id: string;
  timestamp: string;
  severity: string;
  source_type: string;
  service_name: string;
  host: string;
  host_ip: string;
  file_path: string;
  message: string;
  raw_message: string;
  trace_id: string;
  span_id: string;
  metadata: string;
}

export interface TopError {
  message: string;
  occurrences: number;
  services: string[];
}

export interface TopService {
  service_name: string;
  logs: number;
  errors: number;
  error_ratio: number;
}

// API functions matching your FastAPI endpoints
export const getLogs = async (params: {
  time_range?: string;
  log_level?: string;
  service_name?: string;
  limit?: number;
}): Promise<LogEntry[]> => {
  const response = await apiClient.get('/get_logs', { params });
  return response.data;
};

export const getTopErrors = async (time_range: string = '1h', limit: number = 20): Promise<TopError[]> => {
  const response = await apiClient.get('/dashboard/top_errors', {
    params: { time_range, limit },
  });
  return response.data;
};

export const getTopServices = async (time_range: string = '1h'): Promise<TopService[]> => {
  const response = await apiClient.get('/dashboard/top_services', {
    params: { time_range },
  });
  return response.data;
};

export const getServices = async (time_range: string = '24h'): Promise<{ service_name: string; last_seen: string }[]> => {
  const response = await apiClient.get('/dashboard/services', {
    params: { time_range },
  });
  return response.data;
};

export const getErrorHeatmap = async (time_range: string = '6h'): Promise<any[]> => {
  const response = await apiClient.get('/dashboard/error_heatmap', {
    params: { time_range },
  });
  return response.data;
};

export const suggestFix = async (log_id: string): Promise<any> => {
  const response = await apiClient.post('/suggest', { log_id });
  return response.data;
};
