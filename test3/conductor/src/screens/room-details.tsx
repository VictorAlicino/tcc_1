import { useEffect, useState, useCallback } from "react";
import { TouchableOpacity, ActivityIndicator } from "react-native";

import { Icon } from "@/components/icon";
import { SafeAreaView } from "@/components/safe-area-view";
import { Text } from "@/components/text";
import { StackItemProps } from "@/routes/protected-routes";
import { DeviceData, RoomData } from "@/models/opus-models";
import { buildings } from "@/screens/home";
import { FlatList } from "react-native-gesture-handler";
import { DeviceItem } from "@/components/device-item";

export function RoomDetails({ navigation, route }: StackItemProps<"RoomDetails">) {
  const { roomId, buildings } = route.params;

  const [room, setRoom] = useState<RoomData | null>(null);
  const [spaceName, setSpaceName] = useState("");
  const [loading, setLoading] = useState(true);
  const [currentBuilding, setCurrentBuilding] = useState("");

  useEffect(() => {
    const fetchRoomDetails = async () => {
      const data = buildings.flatMap((b) => b.spaces.flatMap((s) => s.rooms)).find((r) => r.building_room_pk === roomId);
      if (data) {
        setRoom(data);
        setSpaceName(buildings.flatMap((b) => b.spaces).find((s) => s.rooms.includes(data))?.space_name || "");
      }
      setLoading(false);
    };

    fetchRoomDetails();
  }, [roomId]);

  const handleGoBack = useCallback(() => {
    navigation.goBack();
  }, [navigation]);

  if (loading) {
    return (
      <SafeAreaView className="flex-1 items-center justify-center">
        <ActivityIndicator size="large" color="#888" />
      </SafeAreaView>
    );
  }

  const handleOnPress = (device: DeviceData) => {
    switch(device.device_type) {
      case "HVAC":
        navigation.navigate("HVACControl", { device});
        break;
      case "LIGHT":
        navigation.navigate("LightControl", { device });
        break;
      default:
        break;
    }
  }

  return (
    <SafeAreaView className="p-2">
      <Text className="text-3xl font-700 mt-8 ml-3">{room?.room_name}</Text>
      {spaceName && <Text className="opacity-70 text-lg ml-3">{spaceName}</Text>}

      <TouchableOpacity
        className="flex-row items-center my-2 py-2"
        activeOpacity={0.7}
        onPress={handleGoBack}
        accessibilityLabel="Voltar para a seleção de salas"
      >
        <Icon name="chevron-left" size={32} />
        <Text className="font-500 uppercase">Selecione outra sala</Text>
      </TouchableOpacity>

      <FlatList
        data={room?.devices || []}
        keyExtractor={(item) => String(item.device_pk)}
        numColumns={2}
        contentContainerStyle={{ paddingHorizontal: 8 }}
        columnWrapperStyle={{ justifyContent: "space-between", marginBottom: 16 }}
        renderItem={({ item }) => (
          <DeviceItem device={item} onPress={ () => {console.log(buildings); handleOnPress(item)} }/>
        )}
        ListEmptyComponent={
          <Text className="text-center text-lg mt-8">Nenhum dispositivo encontrado nesta sala.</Text>
        }
      />
    </SafeAreaView>
  );
}
