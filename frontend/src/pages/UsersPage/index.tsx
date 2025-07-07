
import styles from "./index.module.css"
import { useThemeStore } from "@/store/themeStore";
import Friends from "@/components/Friends";
import Button from "@/components/Button";
import FriendSvg from "@/assets/icons_svg/add_friend.svg?react"
import { useNavigate, useParams } from "react-router-dom";
import { useFilteredFriends } from "@/utils/filterUsers";
import { useState } from "react";

import { useDebounceValue } from "usehooks-ts";
import { useFriends } from "@/hooks/friends/useFriends";
import { useAllUsers } from "@/hooks/users/useAllUsers";
import clsx from "clsx";


export type UsersType ={
  usersType: "users" | "friends" | "admin"
}

const UsersPage = ({usersType}: UsersType) => {
  const { userId } = useParams();
  
  const {theme} = useThemeStore();
  const check_dark = theme === 'dark'
  const navigate = useNavigate()
  
  
  const {friends, isLoading, addFriend, removeFriend} = useFriends(userId)
  const {users, refetchUsers} = useAllUsers()


  
  const [searchQuery, setSearchQuery] = useState<string>("")
  const [debouncedQuery] = useDebounceValue(searchQuery, 300);
  
  const funButton = usersType === 'friends' ? removeFriend : addFriend
  
  const AdminFuncButton =  (id: string) => {
        navigate(`/admin/${id}`)
    }
 

 

  const filteredFriends = useFilteredFriends({
    friends: friends,
    searchQuery:debouncedQuery,
    users: users,
    typeUser: usersType
  })


  
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value)
  }

  if (isLoading) {
    return <div>Loading...</div>
  }
  
  
  const handleAddFriend = () => {
    if (userId) {
      console.log("before")
      console.log("userId:", userId)
     
      navigate(`/admin/${userId}/users`)
      console.log("Navigate to admin page")
    } else {
      navigate('/profile/users')
    }

    if (!users){
      refetchUsers()
    }
    
  }
  
  
  return (

    <div className={clsx(styles.container, check_dark && styles.dark)}>
      <div className={styles.header}>
        <input type="text"
         placeholder=" Search user..." 
         value={searchQuery} 
         onChange={handleSearch}
        />
        { usersType === 'friends' && 
          <Button onClick={handleAddFriend}>
            <FriendSvg />
            Add Friend
          </Button>
        }
      </div>
   
      {
       
      !friends && !users || filteredFriends.length < 1 
      ? <div>
        No {usersType === 'friends' ? 'friends' : 'users'} found
      </div> 
      :<Friends
         onClick={
            usersType !== 'admin' || userId 
            ? (id: number) => funButton(id)
            : (id: number) => AdminFuncButton(id.toString())
         }
         friends={filteredFriends} 
         isDark={check_dark} 
      >

        {usersType === 'admin' 
          ? 'Edit'
          : usersType === 'friends' 
            ? "Remove" 
            : "Add"}
      </Friends>}
    </div>
    
  )
}

export default UsersPage