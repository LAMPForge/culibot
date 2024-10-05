import api from "@/libs/api-client.ts";
import {ICurrentUser} from "../types/user.types.ts";

export async function getMyProfile() {
  const req = await api.post<ICurrentUser>("/users/me");
  return req.data as ICurrentUser;
}