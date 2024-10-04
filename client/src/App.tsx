import {Navigate, Route, Routes} from "react-router-dom";
import {Error404} from "@/components/ui/errors/error-404.tsx";
import LoginPage from "@/pages/auth/login.tsx";

function App() {
  return (
    <>
      <Routes>
        <Route index element={<Navigate to="/home" />} />
        <Route path={"/login"} element={<LoginPage />} />
        <Route path="*" element={<Error404 />} />
      </Routes>
    </>
  )
}

export default App