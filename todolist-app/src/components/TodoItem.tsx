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
    <div className="mb-2">
      <p>id: {todo.id}</p>
      <div className="mb-2">Created at: {todo.time}</div>
      {todo.image ? (
	<img src={todo.image} alt="todo image" className="img-thumbnail" width={300} />
      ) : null}
      <div className="w-25">
	<label className="form-label">Title</label>
	<input className="form-control" value={title} onChange={(e) => setTitle(e.target.value)} />
      </div>
      <div className="w-25">
	<label className="form-label">Description</label>
	<textarea className="form-control" value={description} onChange={(e) => setDescription(e.target.value)}></textarea>
      </div>
      <button className="btn btn-primary mt-2" onClick={handleUpdate}>Update</button>
      <button className="btn btn-danger mt-2" onClick={handleDelete}>Delete</button>
    </div>
  );
}
