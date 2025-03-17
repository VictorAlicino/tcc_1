import { createContext, useContext, useState, useEffect } from "react";
import { api } from "../services/api";
import * as SecureStore from 'expo-secure-store';
import { GoogleSignin, GoogleSigninButton, statusCodes } from "@react-native-google-signin/google-signin";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { conductorUser, conductorToken } from "@/models/conductor_models";
import { loginToConductor } from "@/services/conductor-api";
import { ToastAndroid } from "react-native";
import { User } from "@react-native-google-signin/google-signin";

interface AuthenticationContextData {
  isAuthenticated: boolean;
  googleSignIn: () => Promise<void>;
  registerWithGoogle: () => Promise<void>;
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
    GoogleSignin.configure(
      {
        webClientId: '1039253210102-s60u88i78qf04113egr3hrlpecdujk1g.apps.googleusercontent.com',
        offlineAccess: true
      }
    );
  }, []);

  const isAuthenticated = !!conductorUser?.conductorToken;

  function getCurrentUser(): conductorUser | null {
    return conductorUser;
  }

  async function googleSignIn(): Promise<void> {
    try {
      await GoogleSignin.hasPlayServices();
      let Response = (
        await GoogleSignin.signIn().then((response) => {
          return response;
        }).catch((error) => {
          console.log(error);
    }));
      let loginResponse = Response.user;
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
      }).catch(error => { 
        if (error.name === 'AxiosError') { ToastAndroid.show('Usuário não encontrado', ToastAndroid.SHORT); }
      })
      .catch(error => {
          switch (error.name) {
            case 'AbortError':
              console.log("Server out of reach!")
              break;

            case 'User not found':
              ToastAndroid.show('Usuário não encontrado', ToastAndroid.SHORT);
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

  async function registerWithGoogle(): Promise<void> {
    try {
      await GoogleSignin.hasPlayServices();
      let response = (
        await GoogleSignin.signIn().then((response) => {
          return response;
        }).catch((error) => {
          console.log(error);
      }));
      const payload = response.user;
      console.log(payload);
      api.post('/auth/conductor/register', {
        payload
      }).then((response) => {
        if (response.status === 200) {
          ToastAndroid.show('Você já está cadastrado :)', ToastAndroid.SHORT);
        } else if (response.status === 201) {
          ToastAndroid.show('Usuário cadastrado com sucesso!', ToastAndroid.SHORT);
        }
      }, (error) => {
        console.log(error);
      }
      );
    }
    catch (error: any) {
      setError(error.message);
      setConductorUser(null);
    }
  }

  function getGoogleUser(): User | null{
    const a = GoogleSignin.getCurrentUser();
    return a;
  }

  function signOut() {
    console.log('Signing out...');
    GoogleSignin.signOut();
    setConductorUser(null);
  }

  return (
    <AuthenticationContext.Provider
      value={{
        isAuthenticated,
        googleSignIn,
        registerWithGoogle,
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