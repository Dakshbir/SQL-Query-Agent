const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://your-backend-url.railway.app/api'  // Update after backend deployment
    : '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});
