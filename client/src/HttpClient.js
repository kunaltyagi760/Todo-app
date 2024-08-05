// src/HttpClient.js

import axios from 'axios';

const httpClient = axios.create({
  baseURL: 'http://localhost:5000', // Adjust the baseURL to match your Flask API endpoint
  headers: {
    'Content-Type': 'application/json',
  },
});

export default httpClient;
