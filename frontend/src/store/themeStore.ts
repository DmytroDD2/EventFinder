import { create } from 'zustand';

type ThemeState = {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}
const getTheme = () => {
  const theme = localStorage.getItem("theme");
  if (!theme) {
    localStorage.setItem("theme", "light");
    return "light";
  } else {
    return theme as 'light' | 'dark';
  }
};


export const useThemeStore = create<ThemeState>((set) => ({
  theme: getTheme(), 
  toggleTheme: () => {
    set((state) => {
      const newTheme = state.theme === 'light' ? 'dark' : 'light';
      localStorage.setItem("theme", newTheme);
      return { theme: newTheme };
    });
  },
}));