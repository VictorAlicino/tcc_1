import { createContext, useContext, useState, useEffect } from "react";
import { api } from "../services/api";
import * as SecureStore from 'expo-secure-store';
import { GoogleSignin, GoogleSigninButton, statusCodes } from "@react-native-google-signin/google-signin";
import AsyncStorage from "@react-native-async-storage/async-storage";


interface AuthenticationContextData {
  isAuthenticated: boolean;
  googleSignIn: () => Promise<void>;
  signOut: () => void;
  getCurrentUser: () => conductorUser | null;
}

interface AuthenticationProviderProps {
  children: React.ReactNode;
}

interface conductorToken{
  access_token?: string | null;
  exp: Date | null;
}

interface conductorUser {
  id: string | null;
  email: string | null;
  name: string | null;
  givenName: string | null;
  familyName: string | null;
  photo: string | null;
  conductorToken?: conductorToken;
}
const AuthenticationContext = createContext({} as AuthenticationContextData);

async function storeToken(token: string): Promise<void> {
  await SecureStore.setItemAsync('googleAccessToken', token);
}

async function getStoredToken(): Promise<string | null> {
  return await SecureStore.getItemAsync('googleAccessToken');
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
      const request = JSON.stringify({
        'email': loginResponse.email,
        'google_sub': loginResponse.id
      })
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 1500);
      await fetch('http://192.168.15.87:9530/auth/conductor/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: request,
        signal: controller.signal
      })
      .then(response => {
          clearTimeout(timeoutId);
          if (response.status === 401) {
              throw new Error('Unauthorized: Invalid credentials or session expired.');
          }
          
          return response.json();
      })
      .then(data => {
          loginResponse.conductorToken = {
              access_token: data.access_token,
              exp: data.exp
          };
          setConductorUser(loginResponse);
          api.defaults.headers.common["Authorization"] = `Bearer ${data.access_token}`;
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
      });
        console.log(loginResponse);

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