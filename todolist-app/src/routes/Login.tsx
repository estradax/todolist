import { gql, useLazyQuery } from "@apollo/client";

const GET_AUTH_URL = gql`
  query {
    auth_url
  }
`;

export default function Login() {
  const [getAuthUrl, response] = useLazyQuery<{ auth_url: string }>(GET_AUTH_URL);

  if (response.loading) {
    return <p>Loading...</p>;
  }

  if (response.error) {
    return <p>error: {response.error.message}</p>;
  }

  if (response.data) {
    window.location.href = response.data.auth_url;
    return;
  }

  return (
    <div className="d-flex flex-column align-items-center mt-4">
      <h1>Welcome to Login page</h1>
      <button className="btn btn-primary" onClick={() => getAuthUrl()}>Login</button>
    </div> 
  );
}
