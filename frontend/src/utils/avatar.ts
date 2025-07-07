
export type DefaultAvatar = {
    firstName: string;
    lastName: string;
    email: string;
  };
  
  export type PhotoUrl = { url: string |"string"};
  
  const AVATAR_COLORS = [
    '#4a6bff',
    '#ff6b6b',
    '#6bff6b', 
    '#ffb86b', 
    '#b46bff',
  ];
  
  export const getInitials = (user: DefaultAvatar): string => {
    return `${user.firstName[0]}${user.lastName[0]}`.toUpperCase();
  };
  
  export const getAvatarColor = (email: string): string => {
    const hash = email.split('').reduce((acc, char) => {
      return char.charCodeAt(0) + acc;
    }, 0);
    
    return AVATAR_COLORS[hash % AVATAR_COLORS.length];
  };
  
