import { TouchableOpacity, TouchableOpacityProps, View } from "react-native";
import { Icon } from "@/components/icon";
import { Text } from "@/components/text";

interface RoomItemProps extends TouchableOpacityProps {
  space: string;
  room: string;
}

export function RoomItem({ space, room, ...props }: RoomItemProps) {
  return (
    <TouchableOpacity 
      className="bg-gray-800 rounded-xl p-4 flex-row items-center justify-between space-x-4"
      activeOpacity={0.7}
      {...props}
    >
      <Icon name="meeting-room" size={36} />
      <View>
        <Text className="opacity-70 font-500 text-right" numberOfLines={1}>{space}</Text>
        <Text className="text-xl font-700 text-right" numberOfLines={1}>{room}</Text>
      </View>
    </TouchableOpacity>
  );
}