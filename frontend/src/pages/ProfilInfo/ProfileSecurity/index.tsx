import Button from "@/components/Button"
import styles from "./index.module.css"
// import { useProfile } from "@/hooks/useProfile";
import { UserAvatar } from "@/components/UserAvatar";
import { Link, useParams } from "react-router-dom";
import Key from "@/assets/icons_svg/key.svg?react";
import Arrow from "@/assets/icons_svg/arrow.svg?react";
// import { useUpdateProfile } from "@/hooks/profile/useUpdateProfile";
import UploadFile from "@/components/UploadFile";
import useUpdateImage from "@/hooks/profile/useUpdateImage";
import clsx from "clsx";


type ProfileData = {
  email: string;
  first_name: string;
  last_name: string;
  profile_picture: string;
};


// 2. Оголосіть компонент з правильними пропсами
interface ProfileSecurityProps {
  profile: ProfileData;
  isDark: boolean;
}

const ProfileSecurity = ({ profile, isDark }: ProfileSecurityProps) => {
  const {userId} = useParams()
  const { updateImage, uploadProgress } = useUpdateImage(userId);

  const handleSubmit = (data: File) => {
    updateImage(data);
  };
  const changePassword = userId ? `/admin/${userId}/password-change` : '/password-change';
  return (
    <div className={ clsx( styles.container, isDark && styles.dark)}>
      <div className={styles.image_container}>
        
      <UserAvatar user={{
          email: profile.email,
          firstName: profile.first_name,
          lastName: profile.last_name,
          url: profile.profile_picture
        }}
        className={styles.avatar}
        />
        <UploadFile
          className={styles.button_upload}
          sendImage={handleSubmit}
          uploadProgress={uploadProgress}
        >
          Upload New Photo
        </UploadFile>
        
        
        <p>Supported formats: JPG, PNG, GIF, HEIC, HEIF</p>

      </div>

      <div className={styles.password_section}>
        <h3>Account Security</h3>

        <Link to={changePassword} className={styles.link}>
          
          <div className={styles.link_text}>
            <Key className={styles.icon}/>
            Change Password
          </div>

          <Arrow className={styles.icon}/>
        </Link>
      </div>
    </div>
  )
}

export default ProfileSecurity