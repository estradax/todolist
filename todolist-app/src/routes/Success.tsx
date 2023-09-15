import { gql, useQuery } from "@apollo/client";
import { Navigate, useSearchParams } from "react-router-dom";

import Loading from "../components/Loading";
import Error from "../components/Error";

const GET_CHECKOUT_SESSION = gql`
  query CheckoutSession($sessionId: String!) {
    checkout_session(sessionId: $sessionId)
  }
`;

export default function Success() {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');

  const { loading, error, data } = useQuery(GET_CHECKOUT_SESSION, {
    variables: {
      sessionId
    }
  });

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <Error msg={error.message} />;
  }

  if (data) {
    if (data.checkout_session === 'complete') {
      return <Navigate to="/" />;
    }
  }

  return <h1>Waiting</h1>;
}
