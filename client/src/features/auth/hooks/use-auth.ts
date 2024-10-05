import {useState} from "react";
import {useNavigate} from "react-router-dom";
import {useAtom} from "jotai";
import {currentUserAtom} from "../../user/atoms/current-user.atom.ts";
import {authLink, authLinkAuthenticate} from "../services/auth-service.ts";
import APP_ROUTE from "../../../libs/app-route.ts";
import {notifications} from "@mantine/notifications";
import {IAuthLinkLogin} from "../types/auth.types.ts";

export default function useAuth() {
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate()

  const [_, setCurrentUser] = useAtom(currentUserAtom);
  // const [authToken, setAuthToken] = useAtom(authTokensAtom);

  const handleAuthLink = async (data: IAuthLinkLogin) => {
    setIsLoading(true);

    try {
      await authLink(data);
      setIsLoading(false);
      navigate(`${APP_ROUTE.AUTH.AUTH_LINK.REQUEST}?email=${encodeURIComponent(data.email)}`);
    } catch (e) {
      setIsLoading(false);
      notifications.show({
        message: e.response?.data.message,
        color: "red",
      });
    }
  }

  const handleAuthLinkAuthenticate = async (token: string) => {
    setIsLoading(true);

    try {
      const res = await authLinkAuthenticate(token);
      console.log(res);
      setIsLoading(false);
      navigate(APP_ROUTE.HOME);
    } catch (e) {
      console.log(e);
      setIsLoading(false);
      notifications.show({
        message: e.response?.data.message,
        color: "red"
      });
    }
  }

  return {
    isLoading,
    handleAuthLink,
    handleAuthLinkAuthenticate
  }
}
