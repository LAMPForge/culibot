import { atomWithStorage } from "jotai/utils";
import {ICurrentUser} from "../types/user.types.ts";
import {focusAtom} from "jotai-optics";

export const currentUserAtom = atomWithStorage<ICurrentUser | null>(
  "currentUser",
  null
);

export const userAtom = focusAtom(currentUserAtom, (optic) =>
  optic.prop("user"),
);
