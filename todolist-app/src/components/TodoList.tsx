import { Todo } from "../todo";
import TodoItem from "./TodoItem";

export default function TodoList({ todos }: { todos: Todo[] }) {
  return (
    <ul>
      {todos.map((todo) => (
	  <li key={todo.id}>
	    <TodoItem todo={todo} />
	  </li>
	)
      )}
    </ul>
  );
}
