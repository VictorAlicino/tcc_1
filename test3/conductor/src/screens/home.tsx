import { useState } from "react";
import { ScrollView, View, TouchableOpacity } from "react-native";
import { clsx } from "clsx";

import { Icon } from "@/components/icon";
import { SafeAreaView } from "@/components/safe-area-view";
import { Text } from "@/components/text";
import { SearchBar } from "@/components/search-bar";
import { RoomItem } from "@/components/room-item";

const spaces = [
  {
    id: "ALL",
    name: "Todos",
  },
  {
    id: "1234",
    name: "Espaço 01",
  },
  {
    id: "1233",
    name: "Espaço 02",
  },
  {
    id: "1232",
    name: "Espaço 03",
  },
  {
    id: "1231",
    name: "Espaço 04",
  },
];

const rooms = [
  {
    id: "1",
    name: "Sala 01",
    spaceId: "1234",
  },
  {
    id: "2",
    name: "Sala 02",
    spaceId: "1234",
  },
  {
    id: "3",
    name: "Sala 03",
    spaceId: "1234",
  },
  {
    id: "4",
    name: "Sala 04",
    spaceId: "1233",
  },
  {
    id: "5",
    name: "Sala 05",
    spaceId: "1232",
  },
]

export function Home() {
  const [currentSpace, setCurrentSpace] = useState({
    id: "ALL",
    name: "Todos",
  });

  const filteredRooms = rooms.filter(room => {
    if (currentSpace.id === "ALL") {
      return true;
    }

    return room.spaceId === currentSpace.id;
  });

  return (
    <SafeAreaView>
      <TouchableOpacity 
        className="flex-row space-x-2 items-center self-center px-4" 
        activeOpacity={0.7}
      >
        <Text className="font-500 text-lg">BLOCO 6</Text>
        <Icon name="arrow-drop-down" size={32} />
      </TouchableOpacity>

      <View className="mt-8">
        <SearchBar placeholder="Buscar sala em espaços" />
      </View>

      <View>
        <ScrollView 
          className="mt-4 -mx-4" 
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={{
            gap: 14,
            paddingHorizontal: 16,
          }}
        >
          {spaces.map(space => (
            <TouchableOpacity 
              key={space.id} 
              className="p-1" 
              activeOpacity={0.7}
              onPress={() => setCurrentSpace(space)}
            >
              <Text 
                className={clsx("font-500 uppercase", space.id === currentSpace.id && "text-amber-500 border-b-[3px] border-amber-500 md:border-b-2")}
              >
                {space.name}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>        
      </View>

      <ScrollView className="mt-4 space-y-4" showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingVertical: 16 }}>
        {!filteredRooms.length && (
          <View className="flex-row items-center space-x-2 justify-center">
            <Icon name="no-meeting-room" size={24} />
            <Text className="opacity-70">Você não possui salas nesse espaço!</Text>
          </View>
        )}

        {filteredRooms.map(room => {
          const space = spaces.find(space => space.id === room.spaceId);
          return (
            <RoomItem key={room.id} space={space?.name || currentSpace.name} room={room.name} />
          )
        })}
      </ScrollView>
    </SafeAreaView>
  );
}
