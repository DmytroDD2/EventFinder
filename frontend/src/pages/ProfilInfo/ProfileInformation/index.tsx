
import styles from "./index.module.css"
import Button  from "@/components/Button";
import { useForm, SubmitHandler } from "react-hook-form";
import { useUpdateProfile } from "@/hooks/profile/useUpdateProfile";
import clsx from "clsx";

type ProfileFields = {
  first_name: string;
  last_name: string;
  username: string;
  email: string;
};

type ProfileFieldsTyeme = {
  profile: ProfileFields
  isDark: boolean
}


const ProfileInformation = ({ profile, isDark }: ProfileFieldsTyeme) => {
  const { register, handleSubmit, reset } = useForm<ProfileFields>();
  const {updateProfile} = useUpdateProfile();
  
  const onSubmit: SubmitHandler<ProfileFields> = (data) => {
          const queryParams = new FormData();
          console.log(data)
          if (data.first_name !== profile.first_name) queryParams.append('first_name', data.first_name ?? '');
          if (data.last_name !== profile.last_name) queryParams.append('last_name', data.last_name ?? '');
          if (data.username  !== profile.username) queryParams.append('username', data.username ?? '');
          if (data.email !== profile.email) queryParams.append('email', data.email ?? '');
  
          updateProfile(queryParams);
      };
  


  const handleCancel = () => {
    reset({
      first_name: profile.first_name,
      last_name: profile.last_name,
      username: profile.username,
      email: profile.email
    });
  };

  const profileFields = [
  { label: 'First Name', name: 'first_name', type: 'text', defaultValue: profile.first_name },
  { label: 'Last Name', name: 'last_name', type: 'text', defaultValue: profile.last_name },
  { label: 'Username', name: 'username', type: 'text', defaultValue: profile.username },
  { label: 'Email', name: 'email', type: 'email', defaultValue: profile.email },
];

  return (
    <form 
      onSubmit={handleSubmit(onSubmit)}
      className={clsx(styles.form_container, isDark && styles.dark)}
    >
      <fieldset className={styles.fieldset_container}>
      <legend>Profile Information</legend>
        {profileFields.map(field => (
          <div key={field.name} className={styles.input_container}>
            <label htmlFor={field.name}>{field.label}:</label>
            <input
              type={field.type}
              id={field.name}
              {...register(field.name as keyof ProfileFields)}
              defaultValue={field.defaultValue}
              
            />
          </div>
        ))}

      </fieldset>
      <div className={styles.buttons_container}>
        <Button className={styles.cancel_button} onClick={handleCancel}>Cancel</Button>
        <Button type="submit" className={styles.submit_button}>
             Save Changes
        </Button>
      </div>
    </form>
  )
}

export default ProfileInformation