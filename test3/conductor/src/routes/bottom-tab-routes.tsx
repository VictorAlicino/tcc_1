import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import colors from "tailwindcss/colors";

import { Icon } from "@/components/icon";
import { Home } from "@/screens/home";
import { QRCode } from "@/screens/qr-code";
import { Settings } from "@/screens/settings";

const Tab = createBottomTabNavigator();

export function BottomTabRoutes() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: colors.amber[500],
        tabBarStyle: {
          backgroundColor: colors.zinc[800],
          borderTopWidth: 0,
          height: 60,
          paddingTop: 6,
          paddingBottom: 6,
        },
        tabBarLabelStyle: {
          fontFamily: "Roboto_500Medium",
          fontSize: 13,
        },
      }}
      initialRouteName="Home"
    >
      <Tab.Screen
        name="QRCode"
        component={QRCode}
        options={{
          title: "Ler Código",
          tabBarIcon: ({ color, size }) => <Icon name="qr-code" size={size} color={color} />,
        }}
      />
      <Tab.Screen
        name="Home"
        component={Home}
        options={{
          title: "Início",
          tabBarIcon: ({ color, size }) => <Icon name="home-work" size={size} color={color} />,
        }}
      />
      <Tab.Screen
        name="Settings"
        component={Settings}
        options={{
          title: "Configurações",
          tabBarIcon: ({ color, size }) => <Icon name="settings" size={size} color={color} />,
        }}
      />
    </Tab.Navigator>
  );
}
