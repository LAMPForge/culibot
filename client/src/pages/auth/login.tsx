import {Helmet} from "react-helmet-async";
import {LoginForm} from "@/features/auth/components/login-form.tsx";

export default function LoginPage() {
  return (
    <>
      <Helmet>
        <title>Login - Culibot</title>
      </Helmet>
      <LoginForm />
    </>
  )
}
