import { createNativeStackNavigator, NativeStackScreenProps } from "@react-navigation/native-stack";

import { BottomTabRoutes } from "@/routes/bottom-tab-routes";
import { RoomDetails } from "@/screens/room-details";
import { BuildingData, DeviceData } from "@/models/opus-models";
import { OpusHVAC } from "@/screens/opus_hvac";
import { OpusLight } from "@/screens/opus_light";

type StackParamList = {
  BottomTabRoutes: undefined;
  RoomDetails: {
    roomId: string;
    buildings: BuildingData[]
  };
  HVACControl: {
    device: DeviceData;
  };
  LightControl: {
    device: DeviceData;
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
      <Stack.Screen name="HVACControl" component={OpusHVAC} />
      <Stack.Screen name="LightControl" component={OpusLight} />
    </Stack.Navigator>
  );
}
