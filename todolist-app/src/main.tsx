import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { ApolloClient, ApolloProvider, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

import Dashboard from './routes/Dashboard';
import Login from './routes/Login';
import AuthCallback from './routes/AuthCallback';
import Authenticated from './components/Authenticated';
import Unauthenticated from './components/Unauthenticated';
import CreateTodo from './routes/CreateTodo';

const httpLink = createHttpLink({
  uri: 'http://localhost:5000/graphql',
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('access_token');
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    }
  }
});

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache()
});

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <Authenticated>
	<Dashboard />
      </Authenticated>
    )
  },
  {
    path: '/create-todo',
    element: (
      <Authenticated>
	<CreateTodo />
      </Authenticated>
    )
  },
  {
    path: '/login',
    element: (
      <Unauthenticated>
	<Login />
      </Unauthenticated>
    )
  },
  {
    path: '/auth/cb',
    element: <AuthCallback />
  }
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ApolloProvider client={client}>
      <RouterProvider router={router} />
    </ApolloProvider>
  </React.StrictMode>
);
