import { useNavigation } from "@react-navigation/native";
import { TouchableOpacity, TouchableOpacityProps, View } from "react-native";

import { Icon } from "@/components/icon";
import { Text } from "@/components/text";
import { StackItemProps } from "@/routes/protected-routes";

export interface RoomData {
  id: string;
  name: string;
  spaceId: string;
  devicesCount: number;
}

interface RoomItemProps extends TouchableOpacityProps {
  room: RoomData;
  spaceName: string;
}

export function RoomItem({ room, spaceName, ...props }: RoomItemProps) {
  const navigation = useNavigation<StackItemProps["navigation"]>();
  const devices = room.devicesCount === 1 ? "dispositivo" : "dispositivos";

  function handleNavigateToDetails() {
    navigation.navigate("RoomDetails", {
      roomId: room.id,
    });
  }

  return (
    <TouchableOpacity
      className="bg-zinc-800 rounded-xl p-4 flex-row items-center space-x-5"
      activeOpacity={0.7}
      onPress={handleNavigateToDetails}
      {...props}
    >
      <Icon name="meeting-room" size={36} />
      <View className="flex-1">
        <View className="flex-row items-center justify-between">
          <Text className="opacity-70 text-sm font-500" numberOfLines={1}>
            {spaceName}
          </Text>
          <Text className="opacity-70 text-sm font-500" numberOfLines={1}>
            {!room.devicesCount ? "Nenhum dispositivo" : `${room.devicesCount} ${devices}`}
          </Text>
        </View>
        <Text className="text-xl font-700" numberOfLines={1}>
          {room.name}
        </Text>
      </View>
    </TouchableOpacity>
  );
}
