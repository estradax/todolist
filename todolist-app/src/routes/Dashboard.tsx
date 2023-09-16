import { gql, useQuery } from "@apollo/client";
import { Link } from "react-router-dom";

import { useAuth } from "../hooks/auth";
import { Todo } from "../todo";
import Loading from "../components/Loading";
import Error from "../components/Error";
import TodoList from "../components/TodoList";
import BecomePro from "../components/BecomePro";

const GET_TODOS = gql`
  query GetTodos {
    todos {
      id
      user_id
      title
      description
      image
      time
    }
    is_pro
  }
`;

export default function Dashboard() {
  const { userInfo } = useAuth();
  const { loading, error, data } = useQuery<{ todos: Todo[], is_pro: boolean }>(GET_TODOS);

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <Error msg={error.message} />;
  }

  if (!data) return;

  return (
    <div className="p-4">
      <p>UserId: {userInfo.sub}</p>
      <p>Username: {userInfo.preferred_username}</p>
      <p>Pro: {data.is_pro ? 'True' : 'False'}</p>
      <Link className="btn btn-link" to="/create-todo">Create Todo</Link>
      {data.is_pro ? null : <BecomePro />}
      <TodoList todos={data.todos} />
    </div>
  );
}
