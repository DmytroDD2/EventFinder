import React from 'react';

import {
  DefaultAvatar,
  PhotoUrl,
  getInitials,
  getAvatarColor
} from '../utils/avatar';




type UserAvatarProps = {
  user: DefaultAvatar & PhotoUrl;
  className?: string;
}

export const UserAvatar: React.FC<UserAvatarProps> = ({
  user,
  className = '',
}) => {
  const isDefaultAvatar = user.url !== "string" && user.url;


  if (isDefaultAvatar) {
    return (
      <div
        className={className}
        style={{
          backgroundImage: `url(${user.url})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
        }}
      >
      </div>
    );
  }

  return (
    <div
      className={className}
      style={{
        backgroundColor: getAvatarColor(user.email),
        textAlign: 'center',
        padding: "0",
       
      }}
    >
      {getInitials(user)}
    </div>
  );
};