import { createNativeStackNavigator, NativeStackScreenProps } from "@react-navigation/native-stack";

import { BottomTabRoutes } from "@/routes/bottom-tab-routes";
import { RoomDetails } from "@/screens/room-details";

type StackParamList = {
  BottomTabRoutes: undefined;
  RoomDetails: {
    roomId: string;
  };
};

export type StackItemProps<T extends keyof StackParamList = any> = NativeStackScreenProps<StackParamList, T>;

const Stack = createNativeStackNavigator<StackParamList>();

export function ProtectedRoutes() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
      }}
    >
      <Stack.Screen name="BottomTabRoutes" component={BottomTabRoutes} />
      <Stack.Screen name="RoomDetails" component={RoomDetails} />
    </Stack.Navigator>
  );
}
