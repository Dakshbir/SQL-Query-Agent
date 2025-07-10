import axios from 'axios';
import { useState } from 'react';

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://sql-query-agent-production.up.railway.app/api'  // Your actual Railway URL
    : '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export function useGenerateSQL() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateSQL = async (query: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post('/generate-sql', { query });
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to generate SQL');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { generateSQL, loading, error };
}

export function useCorrectSQL() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const correctSQL = async (query: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post('/correct-sql', { query });
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to correct SQL');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { correctSQL, loading, error };
}

export function useSchema() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSchema = async (refresh = false) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/schema${refresh ? '?refresh=true' : ''}`);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch schema');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { fetchSchema, loading, error };
}

export default api;
