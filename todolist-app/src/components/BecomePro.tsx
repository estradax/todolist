import { gql, useMutation } from "@apollo/client";

import Loading from "./Loading";
import Error from "./Error";

const CREATE_CHECKOUT_SESSION = gql`
  mutation {
    create_checkout_session
  }
`;

export default function BecomePro() {
  const [becomePro, { loading, error, data }] = useMutation(CREATE_CHECKOUT_SESSION);

  if (loading) {
    return <Loading />
  }

  if (error) {
    return <Error msg={error.message} />
  }

  if (data) {
    window.location.href = data.create_checkout_session;
    return;
  }

  return <button onClick={() => becomePro()}>Become pro</button>;
}
