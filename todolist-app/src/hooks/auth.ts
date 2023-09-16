import { gql, useLazyQuery, useQuery } from "@apollo/client";
import { useEffect } from "react";

const GET_USER_INFO = gql`
  query {
    userinfo {
      sub
      preferred_username
    }
  }
`;

const GET_NEW_TOKEN = gql`
  query RefreshToken($refresh_token: String!) {
    refresh_token(refresh_token: $refresh_token) {
      access_token
      refresh_token
    }
  }
`;

// wrapper around useQuery to get userInfo
export function useAuth() {
  const { loading, error, data } = useQuery(GET_USER_INFO);
  const [getNewToken] = useLazyQuery(GET_NEW_TOKEN);

  useEffect(() => {
    const signinInterval = setInterval(async () => {
      const refreshToken = localStorage.getItem('refresh_token'); 
      const res = await getNewToken({
	variables: {
	  refresh_token: refreshToken
	}
      });

      localStorage.setItem('access_token', res.data.refresh_token.access_token);
      localStorage.setItem('refresh_token', res.data.refresh_token.refresh_token);
    }, 15000);

    return () => clearInterval(signinInterval);
  }, []);

  if (loading) {
    console.log('loading');
    return {
      loading,
    }
  }

  if (error) {
    return {
      loading,
      error,
    }
  }

  return {
    loading,
    userInfo: data.userinfo
  }
}
