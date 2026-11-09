/**
 * Cyber Sentinel - Centralized API Service
 * Connects React frontend with the FastAPI backend.
 * Provides unified scanning, ML inference, SSL checks, and health endpoints.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const DEFAULT_TIMEOUT_MS = 15000;

/**
 * Standardized fetch wrapper with timeout and error classification.
 */
async function fetchWithTimeout(endpoint, options = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  const url = `${API_BASE_URL.replace(/\/$/, '')}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...(options.headers || {}),
      },
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      let detailMsg = `HTTP ${response.status}: ${response.statusText}`;
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          detailMsg = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
        }
      } catch (_) {
        // use default error message
      }
      throw new Error(detailMsg);
    }

    return await response.json();
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error(`Request timed out after ${timeoutMs / 1000}s. The target host may be slow or unreachable.`);
    }
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      throw new Error(`Cannot connect to backend at ${API_BASE_URL}. Ensure the FastAPI server is running on port 8000.`);
    }
    throw error;
  }
}

/**
 * Health check endpoint.
 */
export async function checkApiHealth() {
  return await fetchWithTimeout('/', { method: 'GET' }, 4000);
}

/**
 * Full composite Digital Trust scan:
 * Orchestrates ML prediction, SHAP explainability, SSL validation, and Security Headers.
 */
export async function scanUrl(rawUrl) {
  const trimmed = (rawUrl || '').trim();
  if (!trimmed) {
    throw new Error('Please enter a target URL to analyze.');
  }

  const startTime = performance.now();
  const data = await fetchWithTimeout('/scan', {
    method: 'POST',
    body: JSON.stringify({ url: trimmed }),
  });

  const clientLatency = `${(performance.now() - startTime).toFixed(0)} ms`;
  return {
    ...data,
    clientLatency,
  };
}

/**
 * Fast ML-only URL prediction.
 */
export async function predictUrl(rawUrl) {
  const trimmed = (rawUrl || '').trim();
  if (!trimmed) {
    throw new Error('Please enter a target URL to analyze.');
  }

  const startTime = performance.now();
  const data = await fetchWithTimeout('/predict', {
    method: 'POST',
    body: JSON.stringify({ url: trimmed }),
  });

  const clientLatency = `${(performance.now() - startTime).toFixed(0)} ms`;
  return {
    ...data,
    clientLatency,
  };
}

/**
 * Standalone SSL/TLS validation.
 */
export async function validateSsl(rawUrl) {
  return await fetchWithTimeout('/ssl', {
    method: 'POST',
    body: JSON.stringify({ url: rawUrl }),
  });
}

/**
 * Standalone Security Headers audit.
 */
export async function auditHeaders(rawUrl) {
  return await fetchWithTimeout('/headers', {
    method: 'POST',
    body: JSON.stringify({ url: rawUrl }),
  });
}

export default {
  checkApiHealth,
  scanUrl,
  predictUrl,
  validateSsl,
  auditHeaders,
  API_BASE_URL,
};

