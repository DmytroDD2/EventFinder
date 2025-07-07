import UsersPage from '../UsersPage'

function AdminPage() {
  return (
    <div style={{marginTop: '0.5rem'}}>
      <UsersPage usersType='admin' />
    </div>
  )
}

export default AdminPage