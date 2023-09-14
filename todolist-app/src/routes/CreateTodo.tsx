import { gql, useMutation } from "@apollo/client";
import { FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import Error from "../components/Error";

const CREATE_TODO = gql`
  mutation CreateTodo($input: CreateTodoInput!) {
    create_todo(input: $input) {
      id
    }
  }
`;

export default function CreateTodo() {
  const [createTodo, { error }] = useMutation(CREATE_TODO, {
    refetchQueries: ['GetTodos']
  });

  const navigate = useNavigate();

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();

    // validate form data
    const formData = new FormData(e.currentTarget);

    createTodo({
      variables: {
	input: {
	  title: formData.get('title'),
	  description: formData.get('description')
	}
      }
    });

    navigate('/');
  }

  if (error) {
    return <Error msg={error.message} />;
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="title" name="title" />
      <input type="text" placeholder="description" name="description" />
      <button>submit</button>
    </form>
  );
}
