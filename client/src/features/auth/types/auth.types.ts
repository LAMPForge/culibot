export interface IAuthLinkLogin {
  email: string;
  returnTo?: string;
}

export interface ITokens {
  accessToken: string;
}

export interface ITokenResponse {
  tokens: ITokens;
}
