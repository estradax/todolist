import { gql, useQuery } from "@apollo/client";

const GET_USER_INFO = gql`
  query {
    userinfo {
      sub
      preferred_username
    }
  }
`;

// wrapper around useQuery to get userInfo
export function useAuth() {
  const { loading, error, data } = useQuery(GET_USER_INFO);

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
