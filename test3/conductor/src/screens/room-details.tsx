import { useEffect, useState } from "react";
import { TouchableOpacity } from "react-native";

import { Icon } from "@/components/icon";
import { RoomData } from "@/components/room-item";
import { SafeAreaView } from "@/components/safe-area-view";
import { Text } from "@/components/text";
import { StackItemProps } from "@/routes/protected-routes";
import { rooms, spaces } from "@/screens/home";

export function RoomDetails({ navigation, route }: StackItemProps<"RoomDetails">) {
  const { roomId } = route.params;

  const [room, setRoom] = useState<RoomData | null>(null);
  const [spaceName, setSpaceName] = useState("");

  useEffect(() => {
    (async () => {
      const data = rooms.find((room) => room.id === roomId);

      if (data) {
        const space = spaces.find((space) => space.id === data.spaceId);

        if (space) {
          setSpaceName(space.name);
        }

        setRoom(data);
      }
    })();
  }, []);

  return (
    <SafeAreaView>
      <Text className="text-3xl font-700 mt-4">{room?.name}</Text>
      {spaceName && <Text className="opacity-70 text-lg">{spaceName}</Text>}

      <TouchableOpacity
        className="flex-row items-center space-x-2 my-2 py-2"
        activeOpacity={0.7}
        onPress={navigation.goBack}
      >
        <Icon name="chevron-left" size={32} />
        <Text className="font-500 uppercase">Selecione outra sala</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}
