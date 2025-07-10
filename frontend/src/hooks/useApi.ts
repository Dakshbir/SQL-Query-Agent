import axios from 'axios';
import { useState } from 'react';

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://sql-query-agent-production.up.railway.app/api'
    : '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Hook for generating SQL from natural language
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

// Hook for correcting SQL queries
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

// Hook for fetching database schema
export function useSchema() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [schema, setSchema] = useState<any>(null);

  const fetchSchema = async (refresh = false) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/schema${refresh ? '?refresh=true' : ''}`);
      setSchema(response.data.schema);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to fetch schema');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { fetchSchema, schema, loading, error };
}

export default api;
