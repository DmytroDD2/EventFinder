
import { useAuthStore } from "@/store/authStore";
import { UserLog } from "../types/user";
import api from "./api";



export const login = async (username: string, password: string) => {
  const response = await api.post('users/token', { username, password });
  return response.data;
};

export const register = async (userData: UserLog) => {
  const response = await api.post('/users/register', userData);
  return response.data;
};


export const refreshToken = async () => {
  const refresh = useAuthStore.getState().refreshToken;
  if (!refresh) {
   
    throw new Error('Login error');
  }
 
  const params = new URLSearchParams();
  
  params.append('refresh_token', refresh);

  const response = await api.post('/users/token/refresh', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  useAuthStore.getState().refresh(response.data.access_token);
  return response.data.access_token;
  
};