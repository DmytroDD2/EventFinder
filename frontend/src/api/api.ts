import axios from 'axios';
import { useAuthStore } from '../store/authStore';
import { refreshToken } from './auth';



// const url = 'http://0.0.0.0:8000/'
const url = " http://172.20.10.4:8000/"
const api = axios.create({
  baseURL: url,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});




api.interceptors.response.use(
  (response) => response,
  
  async (error) => {
    const originalRequest = error.config;
    const status = error.response?.status;
    
    const isRefreshRequest = originalRequest.url.includes('/token/refresh');


    if (status === 401 && !originalRequest._retry && !isRefreshRequest) {
      originalRequest._retry = true;
     
      if (isRefreshRequest) {
        useAuthStore.getState().logout();
        return Promise.reject(error);
      }
      try {
        const newToken = await refreshToken();
        originalRequest.headers['Authorization'] = `Bearer ${newToken}`; 
        return api(originalRequest); 
      } catch (refreshError) {
        useAuthStore.getState().logout();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api
