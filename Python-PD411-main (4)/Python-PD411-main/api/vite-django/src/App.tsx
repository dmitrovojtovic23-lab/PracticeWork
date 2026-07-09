import './App.css'
import {Route, Routes} from "react-router";
import HomePage from "./pages/HomePage.tsx";
import RootLayout from "./layouts/RootLayout.tsx";
import LoginPage from "./pages/LoginPage.tsx";
import RegistrationPage from "./pages/RegistrationPage.tsx";
import ProfilePage from "./pages/ProfilePage.tsx";

function App() {

  return (
    <>
      <Routes>
          <Route path="/" element={<RootLayout/>} >
              <Route index element={<HomePage/>}/>
              <Route path={"login"} element={<LoginPage/>}/>
              <Route path="registration" element={<RegistrationPage />}/>
              <Route path="profile" element={<ProfilePage />}/>
          </Route>
      </Routes>
    </>
  )
}

export default App
