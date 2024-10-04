import {Box, Container, TextInput, Title, Button} from "@mantine/core";
import classes from "./auth.module.css";
import { z } from 'zod';
import { useForm, zodResolver } from '@mantine/form';
import {IAuthLinkLogin} from "../types/auth.types.ts";

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

  async function onSubmit(data: IAuthLinkLogin) {
    // await login(data);
  }

  return (
    <Container size={420} my={40} className={classes.container}>
      <Box p="xl" mt={200}>
        <Title order={2} ta="center" fw={800} mb="md">
          CULIBOT
        </Title>
        <form onSubmit={form.onSubmit(onSubmit)}>
          <TextInput
            id="email"
            type="email"
            label="Email"
            placeholder="email@example.com"
            variant="filled"
            {...form.getInputProps("email")}
          />
          <Button type="submit" fullWidth mt="xl" loading={false}>
            Sign In
          </Button>
        </form>
      </Box>
    </Container>
  )
}