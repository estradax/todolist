import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { ApolloClient, ApolloProvider, InMemoryCache } from '@apollo/client';

import Dashboard from './routes/Dashboard';
import Login from './routes/Login';
import AuthCallback from './routes/AuthCallback';
import Authenticated from './components/Authenticated';
import Unauthenticated from './components/Unauthenticated';

const client = new ApolloClient({
  uri: 'http://localhost:5000/graphql',
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
