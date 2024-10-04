import {Helmet} from "react-helmet-async";
import { Title, Text, Button, Container, Group } from "@mantine/core";
import { Link } from "react-router-dom";
import classes from "./error-404.module.css";

export function Error404() {
  return (
    <>
      <Helmet>
        <title>Page not found - SuperNote</title>
      </Helmet>
      <Container className={classes.container}>
        <Title className={classes.title}>404 Page Not Found</Title>
        <Text c="dimmed" size="lg" ta="center" className={classes.description}>
          Sorry, we can't find the page you are looking for.
        </Text>
        <Group justify="center">
          <Button component={Link} to={"/home"} variant="subtle" size="md">
            Take me back to homepage
          </Button>
        </Group>
      </Container>
    </>
  )
}
