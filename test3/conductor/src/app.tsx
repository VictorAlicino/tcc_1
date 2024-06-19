import { Roboto_100Thin, Roboto_300Light, Roboto_400Regular, Roboto_500Medium, Roboto_700Bold, useFonts } from "@expo-google-fonts/roboto";
import { NavigationContainer } from "@react-navigation/native";
import { registerRootComponent } from "expo";
import { StatusBar } from "expo-status-bar";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import colors from "tailwindcss/colors";

import { Loading } from "@/components/loading";
import { Routes } from "@/routes";
import { AuthenticationProvider } from "./contexts/authentication-context";

function App() {
  const [fontsLoaded] = useFonts({
    Roboto_400Regular,
    Roboto_500Medium,
    Roboto_700Bold,
    Roboto_100Thin
  });


  if (!fontsLoaded) {
    return <Loading />;
  }

  return (
    <GestureHandlerRootView style={{ flex: 1, backgroundColor: colors.zinc[900] }}>
      <NavigationContainer>
        <AuthenticationProvider>
          <Routes />
          <StatusBar style="light" />
        </AuthenticationProvider>
      </NavigationContainer>
    </GestureHandlerRootView>
  );
}

registerRootComponent(App);
