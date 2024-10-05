import {createJSONStorage} from "jotai/vanilla/utils/atomWithStorage";
import {ITokens} from "../types/auth.types.ts";
import Cookies from "js-cookie";
import {atomWithStorage} from "jotai/utils";

const cookieStorage = createJSONStorage<ITokens | null>(() => {
  return {
    getItem: () => Cookies.get("authTokens"),
    setItem: (key, value) => Cookies.set(key, value, { expires: 30 }),
    removeItem: (key) => Cookies.remove(key),
  }
})

export const authTokensAtom = atomWithStorage<ITokens | null>(
  "authTokens",
  null,
  cookieStorage,
);
