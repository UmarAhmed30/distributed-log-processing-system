'use client';

import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { getLogs, getErrorHeatmap, suggestFix, LogEntry, getTopErrors, getTopServices, getServices, TopError, TopService } from '@/lib/api';

export default function Home() {
  // State for logs and filters
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedLog, setSelectedLog] = useState<LogEntry | null>(null);
  const [suggestion, setSuggestion] = useState<string>('');
  const [loadingSuggestion, setLoadingSuggestion] = useState(false);

  // Filter states
  const [timeRange, setTimeRange] = useState('24h');
  const [logLevel, setLogLevel] = useState('');
  const [serviceName, setServiceName] = useState('');
  const [limit, setLimit] = useState(50);
  const [statsView, setStatsView] = useState('');

  // Stats data
  const [topErrors, setTopErrors] = useState<TopError[]>([]);
  const [topServices, setTopServices] = useState<TopService[]>([]);
  const [activeServices, setActiveServices] = useState<{service_name: string; last_seen: string}[]>([]);

  // Heatmap data
  const [heatmapData, setHeatmapData] = useState<any[]>([]);

  // Fetch logs on component mount and when filters change
  useEffect(() => {
    fetchLogs();
    fetchHeatmap();
  }, [timeRange, logLevel, serviceName, limit]);

  // Fetch stats when statsView changes
  useEffect(() => {
    if (statsView === 'top_errors') {
      fetchTopErrors();
    } else if (statsView === 'top_services') {
      fetchTopServices();
    } else if (statsView === 'active_services') {
      fetchActiveServices();
    }
  }, [statsView, timeRange]);

  const fetchLogs = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getLogs({
        time_range: timeRange,
        log_level: logLevel || undefined,
        service_name: serviceName || undefined,
        limit,
      });
      setLogs(data);
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to fetch logs';
      setError(errorMsg);
      console.error('Error fetching logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchHeatmap = async () => {
    try {
      const data = await getErrorHeatmap(timeRange);
      setHeatmapData(data);
    } catch (error: any) {
      // Silently handle heatmap errors - it's not critical
      if (error.response?.status !== 404) {
        console.warn('Error fetching heatmap:', error.message);
      }
    }
  };

  const fetchTopErrors = async () => {
    try {
      const data = await getTopErrors(timeRange, 20);
      setTopErrors(data);
    } catch (error: any) {
      console.warn('Error fetching top errors:', error.message);
    }
  };

  const fetchTopServices = async () => {
    try {
      const data = await getTopServices(timeRange);
      setTopServices(data);
    } catch (error: any) {
      console.warn('Error fetching top services:', error.message);
    }
  };

  const fetchActiveServices = async () => {
    try {
      const data = await getServices(timeRange);
      setActiveServices(data);
    } catch (error: any) {
      console.warn('Error fetching active services:', error.message);
    }
  };

  const handleLogClick = (log: LogEntry) => {
    setSelectedLog(log);
    setSuggestion('');
  };

  const handleSuggestFix = async () => {
    if (!selectedLog) return;
    setLoadingSuggestion(true);
    try {
      const data = await suggestFix(selectedLog.log_id);
      setSuggestion(data.analysis || 'No suggestion available');
    } catch (error) {
      console.error('Error getting suggestion:', error);
      setSuggestion('Failed to get suggestion. Please try again.');
    } finally {
      setLoadingSuggestion(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toUpperCase()) {
      case 'ERROR': return 'bg-red-100 text-red-800 border-red-300';
      case 'WARN': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'INFO': return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'DEBUG': return 'bg-gray-100 text-gray-800 border-gray-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* Title */}
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Distributed Log Processing System</h1>

      {/* Filter Bar */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-lg font-bold text-gray-900 mb-4">Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-2">Time Range</label>
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="1h">Last 1 Hour</option>
              <option value="6h">Last 6 Hours</option>
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-2">Log Level</label>
            <select
              value={logLevel}
              onChange={(e) => setLogLevel(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Levels</option>
              <option value="ERROR">ERROR</option>
              <option value="WARN">WARN</option>
              <option value="INFO">INFO</option>
              <option value="DEBUG">DEBUG</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-2">Service Name</label>
            <input
              type="text"
              value={serviceName}
              onChange={(e) => setServiceName(e.target.value)}
              placeholder="Enter service name"
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-2">Limit</label>
            <input
              type="number"
              value={limit}
              onChange={(e) => setLimit(parseInt(e.target.value))}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
              min="1"
              max="1000"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-800 mb-2">Stats</label>
            <select
              value={statsView}
              onChange={(e) => setStatsView(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-gray-900 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">None</option>
              <option value="top_errors">Top Errors</option>
              <option value="top_services">Top Services</option>
              <option value="active_services">Active Services</option>
            </select>
          </div>
        </div>
      </div>

      {/* Stats Display Section */}
      {statsView && (
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-lg font-bold text-gray-900 mb-4">
            {statsView === 'top_errors' && 'Top Errors'}
            {statsView === 'top_services' && 'Top Services'}
            {statsView === 'active_services' && 'Active Services'}
          </h2>

          {statsView === 'top_errors' && (
            <div className="space-y-3">
              {topErrors.length === 0 ? (
                <div className="text-center py-4 text-gray-500">No error data available</div>
              ) : (
                topErrors.map((error, idx) => (
                  <div key={idx} className="border border-gray-200 rounded p-4">
                    <div className="flex justify-between items-start mb-2">
                      <span className="font-semibold text-red-600">Occurrences: {error.occurrences}</span>
                      <span className="text-sm text-gray-600">Services: {error.services.join(', ')}</span>
                    </div>
                    <p className="text-gray-800">{error.message}</p>
                  </div>
                ))
              )}
            </div>
          )}

          {statsView === 'top_services' && (
            <div className="overflow-x-auto">
              {topServices.length === 0 ? (
                <div className="text-center py-4 text-gray-500">No service data available</div>
              ) : (
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Service</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Total Logs</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Errors</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Error Rate</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {topServices.map((service, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="px-4 py-3 font-medium text-gray-900">{service.service_name}</td>
                        <td className="px-4 py-3 text-gray-700">{service.logs}</td>
                        <td className="px-4 py-3 text-red-600">{service.errors}</td>
                        <td className="px-4 py-3 text-gray-700">{(service.error_ratio * 100).toFixed(2)}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}

          {statsView === 'active_services' && (
            <div className="overflow-x-auto">
              {activeServices.length === 0 ? (
                <div className="text-center py-4 text-gray-500">No service data available</div>
              ) : (
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Service Name</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Last Seen</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {activeServices.map((service, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="px-4 py-3 font-medium text-gray-900">{service.service_name}</td>
                        <td className="px-4 py-3 text-gray-700">{new Date(service.last_seen).toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      )}

      {/* Logs Table */}
      <div className="bg-white rounded-lg shadow mb-8">
        <div className="p-6">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Logs</h2>
          {error ? (
            <div className="bg-red-50 border border-red-200 rounded p-4 text-red-800">
              <p className="font-semibold">Error loading logs:</p>
              <p>{error}</p>
            </div>
          ) : loading ? (
            <div className="text-center py-8 text-gray-500">Loading logs...</div>
          ) : logs.length === 0 ? (
            <div className="text-center py-8 text-gray-500">No logs found</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 border-b">
                  <tr>
                    <th className="px-4 py-3 text-left font-medium text-gray-700">Timestamp</th>
                    <th className="px-4 py-3 text-left font-medium text-gray-700">Severity</th>
                    <th className="px-4 py-3 text-left font-medium text-gray-700">Service</th>
                    <th className="px-4 py-3 text-left font-medium text-gray-700">Host</th>
                    <th className="px-4 py-3 text-left font-medium text-gray-700">Message</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((log, index) => (
                    <tr
                      key={index}
                      onClick={() => handleLogClick(log)}
                      className="border-b hover:bg-gray-50 cursor-pointer transition-colors"
                    >
                      <td className="px-4 py-3 text-gray-600">
                        {new Date(log.timestamp).toLocaleString()}
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded text-xs font-medium border ${getSeverityColor(log.severity)}`}>
                          {log.severity}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-gray-700">{log.service_name}</td>
                      <td className="px-4 py-3 text-gray-600">{log.host}</td>
                      <td className="px-4 py-3 text-gray-700 max-w-md truncate">{log.message}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Visualization Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-bold text-gray-900 mb-4">Error Overview</h2>
        {heatmapData.length === 0 ? (
          <div className="text-center py-8 text-gray-500">No heatmap data available</div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {heatmapData.map((item, index) => (
              <div key={index} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="text-sm font-medium text-gray-700">{item.service_name}</div>
                <div className="text-xs text-gray-500 mt-1">{item.severity}</div>
                <div className="text-2xl font-bold text-gray-900 mt-2">{item.count}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal for Log Details */}
      {selectedLog && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          onClick={() => setSelectedLog(null)}
        >
          <div
            className="bg-white rounded-lg max-w-3xl w-full max-h-[80vh] overflow-y-auto p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-bold text-gray-900">Log Details</h2>
              <button
                onClick={() => setSelectedLog(null)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ×
              </button>
            </div>

            <div className="space-y-3 mb-6">
              <div><span className="font-semibold text-gray-900">Timestamp:</span> <span className="text-gray-900">{new Date(selectedLog.timestamp).toLocaleString()}</span></div>
              <div><span className="font-semibold text-gray-900">Severity:</span> <span className={`px-2 py-1 rounded text-xs ${getSeverityColor(selectedLog.severity)}`}>{selectedLog.severity}</span></div>
              <div><span className="font-semibold text-gray-900">Service:</span> <span className="text-gray-900">{selectedLog.service_name}</span></div>
              <div><span className="font-semibold text-gray-900">Host:</span> <span className="text-gray-900">{selectedLog.host} ({selectedLog.host_ip})</span></div>
              <div><span className="font-semibold text-gray-900">File Path:</span> <span className="text-gray-900">{selectedLog.file_path}</span></div>
              <div><span className="font-semibold text-gray-900">Trace ID:</span> <code className="bg-gray-100 px-2 py-1 rounded text-sm text-gray-900">{selectedLog.trace_id}</code></div>
              <div><span className="font-semibold text-gray-900">Span ID:</span> <code className="bg-gray-100 px-2 py-1 rounded text-sm text-gray-900">{selectedLog.span_id}</code></div>
              <div><span className="font-semibold text-gray-900">Message:</span> <div className="mt-2 bg-gray-50 p-3 rounded text-gray-900">{selectedLog.message}</div></div>
            </div>

            <div>
              <button
                onClick={handleSuggestFix}
                disabled={loadingSuggestion}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded transition-colors"
              >
                {loadingSuggestion ? 'Analysing with AI...' : 'Analyse with AI'}
              </button>

                {suggestion && (
                  <div className="mt-4 bg-green-50 border border-green-200 rounded p-4">
                    <h3 className="font-semibold text-green-900 mb-2">AI Suggestion:</h3>
                    <div className="prose prose-sm max-w-none text-green-800">
                      <ReactMarkdown
                        components={{
                          h1: ({node, ...props}) => <h1 className="text-xl font-bold mb-2" {...props} />,
                          h2: ({node, ...props}) => <h2 className="text-lg font-bold mb-2" {...props} />,
                          h3: ({node, ...props}) => <h3 className="text-base font-semibold mb-1" {...props} />,
                          p: ({node, ...props}) => <p className="mb-2" {...props} />,
                          ul: ({node, ...props}) => <ul className="list-disc pl-5 mb-2" {...props} />,
                          ol: ({node, ...props}) => <ol className="list-decimal pl-5 mb-2" {...props} />,
                          li: ({node, ...props}) => <li className="mb-1" {...props} />,
                          code: ({node, inline, ...props}: any) => 
                            inline ? 
                              <code className="bg-green-100 px-1 py-0.5 rounded text-sm font-mono" {...props} /> : 
                              <code className="block bg-green-100 p-2 rounded text-sm font-mono overflow-x-auto" {...props} />,
                          pre: ({node, ...props}) => <pre className="bg-green-100 p-2 rounded mb-2 overflow-x-auto" {...props} />,
                          strong: ({node, ...props}) => <strong className="font-bold" {...props} />,
                          em: ({node, ...props}) => <em className="italic" {...props} />,
                        }}
                      >
                        {suggestion}
                      </ReactMarkdown>
                    </div>
                  </div>
                )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

