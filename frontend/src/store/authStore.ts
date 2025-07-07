
import { create } from 'zustand';
import { login} from '@/api/auth';
import { UserRole } from '@/types/user';

interface AuthState {
  user: { email: string; name: string; id: number, role: UserRole } | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  initializeAuth: () => void;
  refresh: (token: string) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  
  
  initializeAuth: () => {
    const token = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    const user = localStorage.getItem('user');

 
    if (token && refreshToken && user) {
      
      set({ 
        token,
        refreshToken,
        user: JSON.parse(user),
        isAuthenticated: true 
      });
    }
  },


  login: async (username: string, password: string) => {
    const data = await login(username, password)

    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    localStorage.setItem('user', JSON.stringify({ 
      id: 0,
      role: 'user' 
    }));
    console.log('data', data);
    set({
       user: data.user,
       token: data.access_token,
       isAuthenticated: true })},

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    set({ user: null, token: null, isAuthenticated: false });
  },

  refresh: (token: string) => {
    localStorage.setItem('access_token', token);
    set({ token });
  },
}));