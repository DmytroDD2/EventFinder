
import * as yup from 'yup';
import { RoleType, TypeInput } from './types/submit';


const createPasswordSchema = (type: TypeInput) => {
  const baseSchema = {
    password: yup.string()
      .required('New password is required')
      .min(8, 'Must be at least 8 characters long')
      .matches(/[A-Z]/, 'Must contain at least one uppercase letter')
      .matches(/[a-z]/, 'Must contain at least one lowercase letter')
      .matches(/[0-9]/, 'Must contain at least one number')
      .matches(/[^A-Za-z0-9]/, 'Must contain at least one special character'),
    confirm_password: yup.string()
      .oneOf([yup.ref('password')], 'Passwords must match')
      .required('Password confirmation is required')
  };

  if (type === 'reset') {
    return yup.object({
      username: yup.string().required('Username is required'),
      password_reset_question: yup.string().required('Password reset question is required'),
      ...baseSchema
    });
  }

  if (type === 'registration') {
    const roleSchema: RoleType[] = ['user', 'admin'];

    return yup.object({
      role: yup.string()
        .oneOf(roleSchema, 'Role must be either user or admin')
        .required('Role is required'),
      first_name: yup.string().required('First name is required'),
      last_name: yup.string().required('Last name is required'),
      password_reset_question: yup.string().required('Password reset question is required'),
      email: yup.string()
        .email('Invalid email')
        .required('Email is required')
        .matches(/^[^\s@]+@[^\s@]+\.[^\s@]+$/, 'Invalid email format'),
      username: yup.string().required('Username is required'),
      ...baseSchema
        });
  }

  return yup.object(baseSchema);
};



const calculatePasswordStrength =(password: string): {
  strength: 'Weak' | 'Medium' | 'Strong';
  percentage: number;
} => {

    let strength: 'Weak' | 'Medium' | 'Strong' = 'Weak';

    if (!password) return { strength, percentage: 0 };
    
    let check = 0;
    if (password.length >= 8) check += 25;
    if (/[A-Z]/.test(password)) check += 25;
    if (/[a-z]/.test(password)) check += 25;
    if (/[0-9]/.test(password)) check += 15;
    if (/[^A-Za-z0-9]/.test(password)) check += 10;

    const percentage = Math.round((check / 100) * 100);

    

    if (percentage >= 75) strength = 'Strong';
    else if (percentage >= 50) strength = 'Medium';

    return { strength, percentage };

    
}



const getPasswordRequirements = (newPassword: string) => {

  return [
    {text: 'At least 8 characters', isValid: newPassword.length >= 8},
    {text: 'One uppercase letter', isValid: /[A-Z]/.test(newPassword)},
    {text: 'One lowercase letter', isValid: /[a-z]/.test(newPassword)},
    {text: 'One number', isValid: /[0-9]/.test(newPassword)},
    {text: 'One special character', isValid: /[^A-Za-z0-9]/.test(newPassword)}
  ];
};






// const eventSchema = yup.object({
//   name: yup.string().required('Event name is required'),
//   // images: yup.array()
//   //   .of(
//   //     yup.mixed().nullable().test('fileSize', 'File size is too large', value => {
//   //       if (!value) return true; // Allow null images
//   //       return value.length <= 5 * 1024 * 1024; // 5MB limit
//   //     })
//   //   )
//   //   .required('At least one image is required'),
//   description: yup.string().required('Description is required'),
//   // price: yup.number()
//   //   .nullable()
//   //   .required('Price is required')
//   //   .min(0, 'Price must be a positive number'),
  
//   total_tickets: yup.number()
//     .transform((value, originalValue) => originalValue === "" ? undefined : value)
//     .required('is required')
//     .min(1, 'Total tickets must be at least 1'),
//   venue: yup.string()
//     .required('Venue is required')
//     .min(3, 'Venue must be at least 3 characters long')
//     .matches(/[A-Za-z]/, 'Venue must contain at least one letter')
// });


export type EventFormTypes = {
  name: string;
  description: string;
  total_tickets: number;
  venue: string;
  price?: number;

//   images?: (Image | string) [];
  data?: string;
};



const eventSchema: yup.ObjectSchema<EventFormTypes> = yup.object().shape({
  name: yup.string().required('Event name is required'),
  description: yup.string().required('Description is required'),
  total_tickets: yup.number()
    .transform((value, originalValue) => originalValue === "" ? undefined : value)
    .required('is required')
    .min(1, 'Total tickets must be at least 1'),
  venue: yup.string()
    .required('Venue is required')
    .min(3, 'Venue must be at least 3 characters long')
    .matches(/[A-Za-z]/, 'Venue must contain at least one letter'),
  price: yup.number().optional(),

//   images: yup.array().of(yup.mixed()).optional(),
  data: yup.string().optional(),
});


export {createPasswordSchema, calculatePasswordStrength, getPasswordRequirements, eventSchema};