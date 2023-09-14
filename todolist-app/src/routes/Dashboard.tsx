import { gql, useQuery } from "@apollo/client";
import { useAuth } from "../hooks/auth";

import { Todo } from "../todo";
import Loading from "../components/Loading";
import Error from "../components/Error";
import TodoList from "../components/TodoList";
import { Link } from "react-router-dom";

const GET_TODOS = gql`
  query GetTodos {
    todos {
      id
      user_id
      title
      description
      time
    }
  }
`;

export default function Dashboard() {
  const { userInfo } = useAuth();
  const { loading, error, data } = useQuery<{ todos: Todo[] }>(GET_TODOS);

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <Error msg={error.message} />;
  }

  if (!data) return;

  return (
    <>
      <p>userinfo: {userInfo.sub} {userInfo.preferred_username}</p>
      <Link to="/create-todo">Create Todo</Link>
      <TodoList todos={data.todos} />
    </>
  );
}
