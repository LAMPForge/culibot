import {useSearchParams} from "react-router-dom";
import useAuth from "../../../features/auth/hooks/use-auth.ts";
import {useEffect} from "react";
import {Helmet} from "react-helmet-async";
import {Avatar, Button, Center, Container, Text, Title} from "@mantine/core";

export default function AuthLinkAuthenticate() {
  const [searchParams] = useSearchParams();
  const { handleAuthLinkAuthenticate, isLoading } = useAuth();
  const token = searchParams.get("token");

  return (
    <>
      <Helmet>
        <title>Auth link confirmation - Culibot</title>
      </Helmet>
      <Container
        fluid
        style={{
          height: '100vh',
          background: 'linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(255,235,235,1) 100%)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Center style={{ flexDirection: 'column' }}>
          <Avatar
            src="https://cdn-icons-png.flaticon.com/512/3207/3207623.png"
            size={80}
            radius="xl"
            mb="md"
          />
          <Text style={{ marginBottom: '10px' }} ta="center">
            To complete the login verification process, please click the button below:
          </Text>
          <Button onClick={() => handleAuthLinkAuthenticate(token)} loading={isLoading}>
            Authenticate
          </Button>
        </Center>
      </Container>
    </>
  );
}