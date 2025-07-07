
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import './App.css';
import AppRouter from './routes/AppRoutes';
import { useAuthStore } from './store/authStore';
import {useEffect} from 'react';



const queryClient = new QueryClient()
function App() {

  const check_tocken = !!localStorage.getItem('access_token');
  const { isAuthenticated, initializeAuth} = useAuthStore();
  
  useEffect(() => {
    console.log("rendering");
    if (!isAuthenticated && check_tocken) {
      initializeAuth();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

  
  if (!isAuthenticated && check_tocken) {
    return (<>Loading</>)}

  return (
    <QueryClientProvider client={queryClient}>
        <AppRouter />
    </QueryClientProvider>
  )
}

export default App
