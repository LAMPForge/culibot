import {useQuery, UseQueryResult} from "@tanstack/react-query";
import {ICurrentUser} from "../types/user.types";
import {getMyProfile} from "../services/user-service.ts";

export default function useCurrentUser(): UseQueryResult<ICurrentUser> {
  return useQuery({
    queryKey: ["currentUser"],
    queryFn: async () => {
      return await getMyProfile();
    }
  })
}