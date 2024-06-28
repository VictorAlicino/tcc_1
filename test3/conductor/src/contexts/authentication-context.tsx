import { createContext, useContext, useState, useEffect } from "react";
import * as SecureStore from 'expo-secure-store';
import { GoogleSignin, GoogleSigninButton, statusCodes } from "@react-native-google-signin/google-signin";
import AsyncStorage from "@react-native-async-storage/async-storage";


interface AuthenticationContextData {
  isAuthenticated: boolean;
  googleSignIn: () => Promise<void>;
  signOut: () => void;
  getCurrentUser: () => GoogleUser | null;
}

interface AuthenticationProviderProps {
  children: React.ReactNode;
}

interface GoogleUser {6
  id: string | null;
  email: string | null;
  name: string | null;
  givenName: string | null;
  familyName: string | null;
  photo: string | null;
}

async function storeToken(token: string): Promise<void> {
  await SecureStore.setItemAsync('googleAccessToken', token);
}

async function getStoredToken(): Promise<string | null> {
  return await SecureStore.getItemAsync('googleAccessToken');
}

const AuthenticationContext = createContext({} as AuthenticationContextData);

export function AuthenticationProvider({ children }: AuthenticationProviderProps) {
  const [error, setError] = useState();
  const [googleUser, setGoogleUser] = useState<GoogleUser | null>(null);
  useEffect(() => {
    GoogleSignin.configure({
      // Adicione sua configuração aqui, se necessário
    });
  }, []);

  const isAuthenticated = !!googleUser;

  function getCurrentUser(): GoogleUser | null {
    return googleUser;
  }

  async function googleSignIn(): Promise<void> {
    try {
      await GoogleSignin.hasPlayServices();
      const loginResponse = await GoogleSignin.signIn();
      setGoogleUser(loginResponse.user);
      console.log(loginResponse);
      setError(null);
      // Request login to the server
      const request = JSON.stringify({
        'email': loginResponse.user.email,
        'google_sub': loginResponse.user.id
      })
      console.log(request)
      await fetch('http://192.168.15.87:9530/auth/conductor_request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: request
      }).then(async (response) => {
        if (response.status === 200) {
          console.log(response.body);
          const token = response.headers.get('Authorization');
          if (token) {
            await storeToken(token);
          }
        }
      });

    } catch (error) {
      setError(error.message);
      setGoogleUser(null);
    }
  }


  function signOut() {
    console.log('signOut');
    GoogleSignin.signOut();
    setGoogleUser(null);
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