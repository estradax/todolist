import { gql, useQuery } from "@apollo/client";

const GET_USER_INFO = gql`
  query UserInfo($access_token: String!) {
    userinfo(access_token: $access_token) {
      sub
      preferred_username
    }
  }
`;

// wrapper around useQuery to get userInfo
export function useAuth() {
  const accessToken = localStorage.getItem('access_token');
  if (!accessToken) {
    return {
      error: 'access token not provided',
      loading: false
    }
  }

  const { loading, error, data } = useQuery(GET_USER_INFO, {
    variables: {
      access_token: accessToken
    }
  });

  if (loading) {
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
