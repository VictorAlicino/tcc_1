import { createContext, useContext, useState, useEffect } from "react";
import { api } from "../services/api";
import * as SecureStore from 'expo-secure-store';
import { GoogleSignin, GoogleSigninButton, statusCodes } from "@react-native-google-signin/google-signin";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { conductorUser, conductorToken } from "@/models/conductor_models";
import { loginToConductor } from "@/services/conductor-api";

interface AuthenticationContextData {
  isAuthenticated: boolean;
  googleSignIn: () => Promise<void>;
  signOut: () => void;
  getCurrentUser: () => conductorUser | null;
}

interface AuthenticationProviderProps {
  children: React.ReactNode;
}

const AuthenticationContext = createContext({} as AuthenticationContextData);

async function storeToken(token: conductorToken): Promise<void> {
  await SecureStore.setItemAsync('conductorAcessToken', token.access_token || '');
  await SecureStore.setItemAsync('conductorAcessTokenExp', token.exp ? token.exp.toString() : '');
}

async function getStoredToken(): Promise<conductorToken> {
  return {
    access_token: await SecureStore.getItemAsync('conductorAcessToken'),
    exp: new Date(await SecureStore.getItemAsync('conductorAcessTokenExp')||'')
  }
}

export function AuthenticationProvider({ children }: AuthenticationProviderProps) {
  const [error, setError] = useState();
  const [conductorUser, setConductorUser] = useState<conductorUser | null>(null);
  useEffect(() => {
    GoogleSignin.configure({
    });
  }, []);

  const isAuthenticated = !!conductorUser?.conductorToken;

  function getCurrentUser(): conductorUser | null {
    return conductorUser;
  }

  async function googleSignIn(): Promise<void> {
    try {
      await GoogleSignin.hasPlayServices();
      let loginResponse: conductorUser = (await GoogleSignin.signIn()).user;
      // Request login to the server
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 1500);
      loginToConductor(loginResponse.email, loginResponse.id)
      .then(data => {
        //console.log(data);
        loginResponse.conductorToken = data;
        setConductorUser(loginResponse);
        api.defaults.headers.common["Authorization"] = `Bearer ${data.access_token}`; // Set the token in the header
        storeToken(data); // Store the token in the secure store
        //console.log(conductorUser);
      })
      .catch(error => {
          switch (error.name) {
            case 'AbortError':
              console.log("Server out of reach!")
              break;
          
            default:
              console.error('Error:', error.message);
              break;
          }
        console.log(loginResponse);
      });

    } catch (error: any) {
      setError(error.message);
      setConductorUser(null);
    }
  }

  function signOut() {
    console.log('signOut');
    GoogleSignin.signOut();
    setConductorUser(null);
  }

  return (
    <AuthenticationContext.Provider
      value={{
        isAuthenticated,
        googleSignIn,
        signOut,
        getCurrentUser
      }}
    >
      {children}
    </AuthenticationContext.Provider>
  )
}

export function useAuthentication() {
  return useContext(AuthenticationContext);
}