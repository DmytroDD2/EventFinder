import { FriendType } from '@/types/friends'
import React, { useState } from 'react'
import { UserAvatar } from '../UserAvatar'
import styles from './index.module.css'
import Button from '../Button'
import clsx from 'clsx'
import {motion, AnimatePresence} from 'framer-motion'

type FriendsProps = {
  friends: FriendType[]
  isDark: boolean
  onClick: (number: number) => void
  children?: React.ReactNode
}


const Friends = ({friends, isDark, onClick, children}: FriendsProps) => {

  const [removedIds, setRemovedIds] = useState<number[]>([]);

  const handleRemove = (id: number) => {
    setRemovedIds((prev) => [...prev, id]);
    onClick(id)
  };

  return (
        <div className={styles.container}>
          <AnimatePresence>
            {friends.map((friend) =>
            !removedIds.includes(friend.id) &&
                <motion.article
                  key={friend.id}
                  initial={{ scale: 1, opacity: 1 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0, opacity: 0 }}
                  // exit={{ x: '-100%', opacity: 0 }}
                  transition={{ duration: 0.4 }}
                  className={clsx(styles.friend_article, isDark && styles.dark)}
                  >
                      <UserAvatar user={{
                        email: friend.email,
                        firstName: friend.first_name,
                        lastName: friend.last_name,
                        url: friend.profile_picture,
                      }}
                      className={styles.avatar}
                      />
          
                  <div className={styles.info}>
                    <h3>{friend.first_name} {friend.last_name}</h3>
                    <Button
                    // onClick={() => removeFriend(friend.id)}
                    onClick={() => handleRemove(friend.id)}
                    >{children}</Button>
                  </div>
                </motion.article>
              )}
                </AnimatePresence>
        </div>
  )
}

export default Friends