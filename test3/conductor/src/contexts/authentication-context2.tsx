import { api } from "@/services/api";
import { createContext, useContext, useState } from "react";
import { AuthSessionResult, Prompt, AccessTokenRequest } from 'expo-auth-session';
import * as WebBrowser from "expo-web-browser";
import * as Google from "expo-auth-session/providers/google";
import * as Google2 from "@react-native-google-signin/google-signin"
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from "@react-native-async-storage/async-storage";

// 1039253210102-uo39aqifeim6k0n687gh9jrvgvs76qcd.apps.googleusercontent.com

WebBrowser.maybeCompleteAuthSession();

interface AuthenticationContextData {
  isAuthenticated: boolean;
  googleSignIn: () => Promise<void>;
  signOut: () => void;
}

interface AuthenticationProviderProps {
  children: React.ReactNode;
}

interface GoogleToken {
  authentication: {
    accessToken: string;
  };
}

interface GoogleUser {
  id: string;
  email: string;
  verified_email: boolean;
  name: string;
  given_name: string;
  family_name: string;
  picture: string;
  locale: string;
  code: string;
}

async function storeToken(token: string): Promise<void> {
  await SecureStore.setItemAsync('googleAccessToken', token);
}

async function getStoredToken(): Promise<string | null> {
  return await SecureStore.getItemAsync('googleAccessToken');
}

const AuthenticationContext = createContext({} as AuthenticationContextData);

export function AuthenticationProvider({ children }: AuthenticationProviderProps) {
  const [googleUser, setGoogleUser] = useState("");
  const [request, response, authenticateUser] = Google.useAuthRequest({
    androidClientId: "1039253210102-uo39aqifeim6k0n687gh9jrvgvs76qcd.apps.googleusercontent.com",
    scopes: [
      'https://www.googleapis.com/auth/userinfo.email',
      'https://www.googleapis.com/auth/userinfo.profile',
    ]
  });

  const isAuthenticated = !!googleUser;

  async function googleSignIn(): Promise<void> {
    try {
      const result: AuthSessionResult = await authenticateUser();
  
      if (result.type !== 'success') {
        console.log(result);
        throw new Error("Erro ao obter o token do Google");
      }

      console.log(result);
  
      const googleToken: GoogleToken = {
        authentication: {
          accessToken: result.params.access_token,
        },
      };
  
      const response = await fetch("https://www.googleapis.com/oauth2/v2/userinfo", {
        headers: {
          Authorization: `Bearer ${googleToken.authentication.accessToken}`,
        },
      });
  
      if (!response.ok) {
        throw new Error("Erro ao obter informações do usuário do Google");
      }
  
      const googleUser: GoogleUser = await response.json();
      
      alert(JSON.stringify(googleUser));
      console.log(JSON.stringify(googleUser));
  
      // Aqui você pode adicionar lógica adicional, como armazenar o usuário em seu estado, enviar para sua API, etc.
    } catch (error) {
      console.error("Erro no Google SignIn:", error);
      alert("Erro ao fazer login com o Google: " + error.message);
    }
  }


  function signOut() {
    setGoogleUser("");
  }

  return (
    <AuthenticationContext.Provider
      value={{
        isAuthenticated,
        googleSignIn,
        signOut,
      }}
    >
      {children}
    </AuthenticationContext.Provider>
  )
}

export function useAuthentication() {
  return useContext(AuthenticationContext);
}