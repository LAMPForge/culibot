import axios, { AxiosInstance } from "axios";
import Cookies from "js-cookie";
import APP_ROUTE from "./app-route.ts";

const api: AxiosInstance = axios.create({
  baseURL: '/api',
  withCredentials: true,
});

api.interceptors.request.use(
  (config) => {
    const tokenData = Cookies.get("authTokens");

    let accessToken: string;
    try {
      accessToken =  tokenData && JSON.parse(tokenData)?.accessToken;
    } catch (e) {
      console.log("Invalid token data", e.message);
      Cookies.remove("authTokens");
    }

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
)

api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          Cookies.remove("authTokens");
          redirectToLogin();
          break;
        case 403:
          break;
        case 404:
          break;
        case 500:
          break;
        default:
          break;
      }
    }
    return Promise.reject(error);
  }
)

function redirectToLogin() {
  if (
    window.location.pathname != APP_ROUTE.AUTH.LOGIN &&
    window.location.pathname != APP_ROUTE.AUTH.SIGN_UP
  ) {
    window.location.href = APP_ROUTE.AUTH.LOGIN;
  }
}

export default api;
