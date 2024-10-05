import api from "@/libs/api-client.ts";
import {IAuthLinkLogin} from "../types/auth.types.ts";
import qs from "qs";

export async function authLink(data: IAuthLinkLogin) {
  await api.post('/auth_link/request', data);
}

export async function authLinkAuthenticate(token: string) {
  const data = qs.stringify({ token });
  return await api.post('/auth_link/authenticate', data, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
}
