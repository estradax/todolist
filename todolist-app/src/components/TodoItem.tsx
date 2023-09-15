import { useState } from 'react';
import { gql, useMutation } from '@apollo/client';

import { Todo }  from '../todo';
import Error from '../components/Error';

const UPDATE_TODO = gql`
  mutation UpdateTodo($id: Int!, $input: UpdateTodoInput!) {
    update_todo(id: $id, input: $input) {
      id
    }
  }
`;

const DELETE_TODO = gql`
  mutation DeleteTodo($id: Int!) {
    delete_todo(id: $id) 
  }
`;

export default function TodoItem({ todo }: { todo: Todo }) {
  const [updateTodo, { error: errorUpdate }] = useMutation(UPDATE_TODO);
  const [deleteTodo, { error: errorDelete }] = useMutation(DELETE_TODO, {
    refetchQueries: ['GetTodos']
  });

  const [title, setTitle] = useState(todo.title);
  const [description, setDescription] = useState(todo.description);

  function handleUpdate() {
    updateTodo({
      variables: {
	id: todo.id,
	input: {
	  title,
	  description
	}
      }
    });
  }

  function handleDelete() {
    deleteTodo({
      variables: {
	id: todo.id
      }
    });
  }

  if (errorUpdate) {
    return <Error msg={errorUpdate.message + 'Update'} />;
  }

  if (errorDelete) {
    return <Error msg={errorDelete.message + 'Delete'} />;
  }

  return (
    <div>
      <p>id: {todo.id}</p>
      <p>user_id: {todo.user_id}</p>
      <img src={todo.image} alt="todo image" />
      <p>title:</p>
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
      <p>description</p>
      <input value={description} onChange={(e) => setDescription(e.target.value)} />
      <p>time: {todo.time}</p>
      <button onClick={handleUpdate}>Update</button>
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
}
