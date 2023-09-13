import { useAuth } from "../hooks/auth";

export default function Dashboard() {
  const { userInfo } = useAuth();

  return <h1>Dashboard: {JSON.stringify(userInfo)}</h1>;
}
