import { useAuthentication } from "@/contexts/authentication-context";
import { ProtectedRoutes } from "@/routes/protected-routes";
import { Login } from "@/screens/login";

export function Routes() {
  const { isAuthenticated } = useAuthentication();
  return isAuthenticated ? <ProtectedRoutes /> : <Login />;
}
