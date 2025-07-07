import { useProfile } from "@/hooks/profile/useProfile";
import styles from "./index.module.css"
import ProfileInformation from "./ProfileInformation"
import ProfileSecurity from "./ProfileSecurity"
import { useThemeStore } from "@/store/themeStore";
import { useParams } from "react-router-dom";


const UserInfo = () => {
  const { userId } = useParams();
  const { profile, isLoading} = useProfile(userId);
  const { theme } = useThemeStore();
  const dark = theme === "dark"
  if (isLoading || !profile) return <div>Loading...</div>;
  return (
    <div className={styles.container}>
      <ProfileSecurity profile={profile} isDark={dark} />
      <ProfileInformation profile={profile} isDark={dark}/>
    </div>
  )
}

export default UserInfo