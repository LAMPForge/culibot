export interface IUser {
  id: string;
  username: string;
  email: string;
}

export interface ICurrentUser {
  user: IUser
}
