
import { Outlet } from "react-router";
import Footer from "@/components/Footer";
import Header from "@/components/Header";
import { useThemeStore } from "@/store/themeStore";


const MainLayout = () => {
  const { theme} = useThemeStore();


  return (
    <div className={`container ${theme}`}>
      <Header />
      <main><Outlet/></main>
      <Footer />
    </div>
  );
};

export default MainLayout;