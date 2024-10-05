import {Navigate, Route, Routes} from "react-router-dom";
import {Error404} from "@/components/ui/errors/error-404.tsx";
import LoginPage from "@/pages/auth/login.tsx";
import LandingPage from "./pages/landing/landing.tsx";
import AuthLinkPage from "./pages/auth/auth-link/auth-link.tsx";
import AuthLinkAuthenticate from "./pages/auth/auth-link/authenticate.tsx";

function App() {
  return (
    <>
      <Routes>
        <Route path={"/"} element={<LandingPage />} />
        <Route path={"/login"} element={<LoginPage />} />
        <Route path={"/login/auth-link/request"} element={<AuthLinkPage />} />
        <Route path={"/login/auth-link/authenticate"} element={<AuthLinkAuthenticate />} />
        <Route path="*" element={<Error404 />} />
      </Routes>
    </>
  )
}

export default App