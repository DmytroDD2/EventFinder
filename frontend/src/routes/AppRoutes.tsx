// src/routes/AppRouter.tsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from '@/pages/HomePage';
import MainLayout from '@/layouts/MainLayout';
import LoginPage from '@/pages/LoginPage';
import ProtectedRoute from '@/components/ProtectedRoute';
import EventDetail from '@/pages/EventDetail';
// import RegisterPage from '@/pages/RegisterPage';
import EventsPage from '@/pages/EventsPage';
import ProfileRoutes from './ProfileRoutes';
import AuthForm from '@/pages/AuthForm';
import RechargePage from '@/pages/RechargePage/ index';
import CreateEventPage from '@/pages/CreateEventPage';
import AdminPage from '@/pages/AdminPage';
// import EventDetailPage from '@/pages/EventDetailPage';
// import ProfilePage from '@/pages/ProfilePage';
// import TicketsPage from '@/pages/TicketsPage';
// import ReviewsPage from '@/pages/ReviewsPage';
// import NotificationsPage from '@/pages/NotificationsPage';


const AppRouter = () => (
  <Router>
    <Routes >
      <Route path="/" element={<MainLayout />}>
        <Route index element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<AuthForm actionType='registration' />} />

        <Route path="password-reset" element={<AuthForm actionType='reset'/>} />
        <Route element={<ProtectedRoute />}>
          <Route path="admin" element={<AdminPage />} />
      
          <Route path="events">
            <Route index element={<EventsPage />} />
            <Route path="create" element={<CreateEventPage />} />
            <Route path="edit/:eventId" element={<CreateEventPage isEditMode={true} />} />
            <Route path=":eventId" element={<EventDetail />} />
          </Route>
          <Route path="password-change" element={<AuthForm actionType='change'/>} />
          <Route path="recharge" element={<RechargePage />} />
          {ProfileRoutes()} 
          {/* <Route path="/profile" element={<ProfilePage />} />
          <Route path="profile/tickets" element={<TicketsPage />} />
          <Route path="profile/reviews" element={<ReviewsPage />} />
          <Route path="profile/notifications" element={<NotificationsPage />} /> */}
        </Route>
        {/* Сторінка 404 */}
        <Route path="*" element={<div>404 - Сторінка не знайдена</div>} />
      </Route>
    </Routes>
  </Router>
);

export default AppRouter;