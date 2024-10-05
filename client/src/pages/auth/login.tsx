import {Helmet} from "react-helmet-async";
import {LoginForm} from "@/features/auth/components/login-form.tsx";
import {Container} from "@mantine/core";

export default function LoginPage() {
  return (
    <>
      <Helmet>
        <title>Login - Culibot</title>
      </Helmet>
      <Container fluid style={{ height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <LoginForm />
      </Container>
    </>
  )
}
