import { useNavigation } from "@react-navigation/native";
import { TouchableOpacity, TouchableOpacityProps, View } from "react-native";
import { useCallback } from "react";
import { BuildingData, RoomData } from "@/models/opus-models";

import { Icon } from "@/components/icon";
import { Text } from "@/components/text";
import { StackItemProps } from "@/routes/protected-routes";

interface RoomItemProps extends TouchableOpacityProps {
  room: RoomData;
  spaceName: string;
  buildings: BuildingData[]
}

export function RoomItem({ room, spaceName, buildings, ...props }: RoomItemProps) {
  const navigation = useNavigation<StackItemProps["navigation"]>();

  const handleNavigateToDetails = useCallback(() => {
    navigation.navigate("RoomDetails", { roomId: room.building_room_pk, buildings, });
  }, [navigation, room.building_room_pk]);

  const deviceCount = room.devices.length;

  return (
    <TouchableOpacity
      className="bg-zinc-800 rounded-xl p-4 flex-row items-center space-x-5"
      activeOpacity={0.7}
      onPress={handleNavigateToDetails}
      accessibilityLabel={`Abrir detalhes da sala ${room.room_name}`}
      {...props}
    >
      <Icon name="meeting-room" size={36} />
      <View className="flex-1">
        <View className="flex-row items-center justify-between">
          <Text className="opacity-70 text-sm font-500" numberOfLines={1}>
            {spaceName}
          </Text>
          <Text className="opacity-70 text-sm font-500" numberOfLines={1}>
            {deviceCount > 0 ? `${deviceCount} ${deviceCount === 1 ? "dispositivo" : "dispositivos"}` : "Nenhum dispositivo"}
          </Text>
        </View>
        <Text className="text-xl font-700" numberOfLines={1}>
          {room.room_name}
        </Text>
      </View>
    </TouchableOpacity>
  );
}
