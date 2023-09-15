import { gql, useMutation, useQuery } from "@apollo/client";
import { FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import Error from "../components/Error";
import Loading from "../components/Loading";

const CREATE_TODO = gql`
  mutation CreateTodo($input: CreateTodoInput!) {
    create_todo(input: $input) {
      id
    }
  }
`;

const GET_IS_PRO = gql`
  query {
    is_pro
  }
`;

const toBase64 = (file: File) => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
});

export default function CreateTodo() {
  const { loading, error, data } = useQuery<{ is_pro: boolean }>(GET_IS_PRO);
  const [createTodo, { error: errorCreate }] = useMutation(CREATE_TODO, {
    refetchQueries: ['GetTodos']
  });

  const navigate = useNavigate();

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();

    // validate form data
    const formData = new FormData(e.currentTarget);

    const image = formData.get('image') as File;

    createTodo({
      variables: {
	input: {
	  title: formData.get('title'),
	  description: formData.get('description'),
	  image: image.size !== 0 ? await toBase64(image) : null
	}
      }
    });

    navigate('/');
  }

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <Error msg={error.message} />;
  }

  if (errorCreate) {
    return <Error msg={errorCreate.message} />;
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="title" name="title" />
      <input type="text" placeholder="description" name="description" />
      {data?.is_pro ? <input type="file" name="image" /> : null}
      <button>submit</button>
    </form>
  );
}
