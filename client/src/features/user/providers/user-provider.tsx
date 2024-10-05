import {PropsWithChildren, useEffect} from "react";
import {useAtom} from "jotai";
import {currentUserAtom} from "../atoms/current-user.atom.ts";
import useCurrentUser from "../hooks/user-current-user.ts";

export function UserProvider({children}: PropsWithChildren) {
  const [_, setCurrentUser] = useAtom(currentUserAtom);
  const {
    data,
    isLoading,
    error,
  } = useCurrentUser();

  useEffect(() => {
    if (data && data.user) {
      setCurrentUser(data);
    }
  }, [data, isLoading]);

  if (isLoading) return <></>

  if (!data?.user) return <></>

  if (error) {
    return <>An error occurred</>;
  }

  return <>{children}</>;
}
