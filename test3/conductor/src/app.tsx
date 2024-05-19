import { Roboto_400Regular, Roboto_500Medium, Roboto_700Bold, useFonts } from "@expo-google-fonts/roboto";
import { NavigationContainer } from "@react-navigation/native";
import { registerRootComponent } from "expo";
import { StatusBar } from "expo-status-bar";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import colors from "tailwindcss/colors";

import { Loading } from "@/components/loading";
import { Routes } from "@/routes";

function App() {
  const [fontsLoaded] = useFonts({
    Roboto_400Regular,
    Roboto_500Medium,
    Roboto_700Bold,
  });

  if (!fontsLoaded) {
    return <Loading />;
  }

  return (
    <GestureHandlerRootView style={{ flex: 1, backgroundColor: colors.zinc[900] }}>
      <NavigationContainer>
        <Routes />
        <StatusBar style="light" />
      </NavigationContainer>
    </GestureHandlerRootView>
  );
}

registerRootComponent(App);
