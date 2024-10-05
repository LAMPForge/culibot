import {Text, TextInput, Button, Grid, Divider, Paper, Group} from "@mantine/core";
import classes from "./auth.module.css";
import { z } from 'zod';
import { useForm, zodResolver } from '@mantine/form';
import { IAuthLinkLogin } from "../types/auth.types.ts";
import useAuth from "../hooks/use-auth.ts";
import GoogleIcon from "../../../components/icons/icon-google.tsx";

const formSchema = z.object({
  email: z
    .string()
    .min(1, { message: "Email is required" })
    .email({ message: "Invalid email address" }),
})

export function LoginForm() {
  const form = useForm<IAuthLinkLogin>({
    validate: zodResolver(formSchema),
    initialValues: {
      email: ""
    },
  });

  const { handleAuthLink, isLoading } = useAuth();

  async function onSubmit(data: IAuthLinkLogin) {
    await handleAuthLink(data);
  }

  return (
    <Paper radius="md" p="xl" withBorder>
      <Text size="lg" fw={500}>
        Welcome to Culibot!
      </Text>
      <Group grow mb="md" mt="md">
        <Button leftSection={<GoogleIcon />} variant="default">
          Sign in with Google
        </Button>
      </Group>
      <Divider label="Or continue with email" labelPosition="center" my="lg" />
      <form onSubmit={form.onSubmit(onSubmit)}>
        <Grid>
          <Grid.Col span={8} pt={0}>
            <TextInput
              id="email"
              type="email"
              placeholder="email@example.com"
              variant="filled"
              className={classes["text-input"]}
              {...form.getInputProps("email")}
            />
          </Grid.Col>
          <Grid.Col span={4} pt={0}>
            <Button type="submit" fullWidth className={classes.button} loading={isLoading}>
              Sign In
            </Button>
          </Grid.Col>
        </Grid>
      </form>
    </Paper>
  )
}
