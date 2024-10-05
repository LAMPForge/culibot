import { Helmet } from "react-helmet-async";
import { useSearchParams } from "react-router-dom";
import { Container, Title, Text, Center, Avatar } from "@mantine/core";

export default function AuthLinkPage() {
  const [searchParams] = useSearchParams();
  const email = searchParams.get('email');

  if (!email) {
    return null;
  }

  return (
    <>
      <Helmet>
        <title>Sign in link sent - Culibot</title>
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
          <Title order={2} style={{ marginBottom: '10px' }}>
            Email with sign in link sent
          </Title>
          <Text fw={700}>
            {email}
          </Text>
          <Text c="dimmed" mt="sm" ta={"center"}>
            An account will be created unless one already exists.
          </Text>
        </Center>
      </Container>
    </>
  )
}
