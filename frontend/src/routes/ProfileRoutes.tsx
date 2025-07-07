
import { Route } from 'react-router-dom';
import ProfileLayout from '@/layouts/ProfileLayout/ProfileLayout';
import ProfilInfo from '@/pages/ProfilInfo';
import TicketsPage from '@/pages/TicketsPage';
import ReviewsPage from '@/pages/ReviewsPage';
import NotificationsPage from '@/pages/NotificationsPage';
import UserEvents from '@/pages/UserEvents';
import UsersPage from '@/pages/UsersPage';
import CreateEventPage from '@/pages/CreateEventPage';
import EventDetail from '@/pages/EventDetail';
import RechargePage from '@/pages/RechargePage/ index';
import AuthForm from '@/pages/AuthForm';



const ProfileRoutes = () => (
    
    <>
  
    <Route path="/profile" element={<ProfileLayout />}>
      <Route index element={<ProfilInfo />} />
      <Route path="users" element={<UsersPage usersType="users" />} />
      <Route path="friends" element={<UsersPage usersType="friends" />} />
      <Route path="tickets" element={<TicketsPage />} />
      <Route path="events" element={<UserEvents />} />
      <Route path="reviews" element={<ReviewsPage />} />
      <Route path="notifications" element={<NotificationsPage />} />
    </Route>

    <Route path="/admin/:userId" element={<ProfileLayout />}>
      <Route index element={<ProfilInfo />} />
      <Route path="password-change" element={<AuthForm actionType='change'/>} />
      <Route path="events/:eventId" element={<EventDetail/>} />
      <Route path="events/edit/:eventId" element={<CreateEventPage isEditMode={true} />} />
      <Route path="recharge" element={<RechargePage />} />
      <Route path="events/create" element={<CreateEventPage />} />
      <Route path="users" element={<UsersPage usersType="admin" />} />
      <Route path="friends" element={<UsersPage usersType="friends" />} />
      <Route path="tickets" element={<TicketsPage />} />
      <Route path="events" element={<UserEvents />} />
      <Route path="reviews" element={<ReviewsPage />} />
      <Route path="notifications" element={<NotificationsPage />} />
    </Route>
  </>
    
  );
  
  export default ProfileRoutes;