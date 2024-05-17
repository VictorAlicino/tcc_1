import { registerRootComponent } from "expo";
import { StatusBar } from "expo-status-bar";
import { 
  useFonts, 
  Roboto_400Regular, 
  Roboto_500Medium, 
  Roboto_700Bold 
} from "@expo-google-fonts/roboto";

import { Home } from "@/screens/home";

function App() {
  const [fontsLoaded] = useFonts({
    Roboto_400Regular,
    Roboto_500Medium,
    Roboto_700Bold
  });

  if (!fontsLoaded) {
    return null;
  }

  return (
    <>
      <Home />
      <StatusBar style="light" />
    </>
  )
}

registerRootComponent(App);
