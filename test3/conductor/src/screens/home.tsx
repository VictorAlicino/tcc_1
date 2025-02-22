import { AnimatePresence, MotiView } from "moti";
import { useEffect, useState } from "react";
import { ScrollView, View } from "react-native";
import { api } from "@/services/api";

import { BuildingButton } from "@/components/building-button";
import { BuildingItem } from "@/components/building-item";
import { EmptyData } from "@/components/empty-data";
import { RoomItem } from "@/components/room-item";
import { BuildingData, DeviceData, RoomData, SpaceData, ApiResponse} from "@/models/opus-models";
import { SafeAreaView, statusBarHeight } from "@/components/safe-area-view";
import { SearchBar } from "@/components/search-bar";
import Spacer from "@/components/spacer";
import { Text } from "@/components/text";
import { TouchableOpacity } from "react-native-gesture-handler";

export let buildings: BuildingData[] = [];

export function Home() {
  const [isLoading, setIsLoading] = useState(true);

  const [currentServerPK, setCurrentServerPK] = useState("");
  const [availableBuildings, setAvailableBuildings] = useState<BuildingData[]>([]);
  const [availableSpaces, setAvailableSpaces] = useState<SpaceData[]>([]);
  const [availableRooms, setAvailableRooms] = useState<RoomData[]>([]);
  const [availableDevices, setAvailableDevices] = useState<DeviceData[]>([]);

  const [buildingsVisible, setBuildingsVisible] = useState(false);
  const [search, setSearch] = useState("");
  const [searchBuilding, setSearchBuilding] = useState("");

  const [currentBuilding, setCurrentBuilding] = useState<BuildingData | null>(null);
  const defaultSpace: SpaceData = { building_space_pk: "ALL", space_name: "Todos", rooms: [] };
  const [currentSpace, setCurrentSpace] = useState<SpaceData>(defaultSpace);

  async function getDataFromServer() {
    try {
      const response = await api.get<ApiResponse>("/users/opus_server/dump")

      const buildings = response.data
      const spaces = buildings.flatMap(building => building.spaces);
      const rooms = spaces.flatMap(space => space.rooms);
      const devices = rooms.flatMap(room => room.devices);

      setAvailableBuildings(buildings);
      setAvailableSpaces(spaces);
      setAvailableRooms(rooms);
      setAvailableDevices(devices);

      if (buildings.length > 0) {
        setCurrentBuilding(buildings[0]);
      }
    } catch (error) {
      console.error("Error fetching buildings:", error);      
    } finally {
      setIsLoading(false);
    } 
  }

  useEffect(() => {
    getDataFromServer()
  }, []);

  useEffect(() => {
    setCurrentSpace(currentBuilding?.spaces[0] ?? defaultSpace);
  }, [currentBuilding]);

  useEffect(() => {
    if (availableBuildings) {
      setIsLoading(false);
    }
  }, [availableBuildings])

  const filteredSpaces = currentBuilding?.spaces ?? [];

  const rooms = filteredSpaces.flatMap(space => space.rooms.map(room => ({
    ...room,
    building_space_pk: space.building_space_pk,
    space_name: space.space_name,
  })));

  const filteredRooms = rooms.filter((room) => {
    if (currentSpace.building_space_pk === "ALL") {
      return filteredSpaces
    }

    return room.building_space_pk === currentSpace.building_space_pk;
  });
  
  const searchRooms = filteredRooms.filter(room =>
    room.room_name.toLowerCase().includes(search.toLowerCase())
  );
  const searchBuildings = availableBuildings.filter(building =>
    building.building_name.toLowerCase().includes(searchBuilding.toLowerCase())
  );

  function handleBuildingChange(building: BuildingData) {
    setCurrentBuilding(building);
    setBuildingsVisible(false);
  }

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 items-center justify-center">

      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView>
      <AnimatePresence>
        {buildingsVisible && (
          <MotiView
            className="absolute left-0 right-0 top-0 bottom-0 z-10 bg-zinc-900 px-4"
            style={{ paddingTop: statusBarHeight }}
            from={{ opacity: 0, translateY: -600 }}
            animate={{ opacity: 1, translateY: 0 }}
            exit={{ opacity: 0, translateY: -600 }}
            transition={{ type: "timing", duration: 400 }}
          >
            <BuildingButton
              title={currentBuilding?.building_name ?? "Selecione um edifício"}
              open={true}
              onPress={() => setBuildingsVisible(false)}
            />

            <View className="mt-4 border-b pb-4 -mx-4 px-4 border-zinc-800">
              <SearchBar
                placeholder="Buscar edifício"
                value={searchBuilding}
                onChangeText={setSearchBuilding}
                onClear={() => setSearchBuilding("")}
              />
            </View>
            
            <ScrollView
              className="space-y-4"
              showsVerticalScrollIndicator={false}
              contentContainerStyle={{ paddingVertical: 16 }}
            >
              {!searchBuildings.length && (
                <EmptyData icon="apartment" message="Nenhum edifício encontrado!" />
              )}

              {searchBuildings.map(building => (
                <BuildingItem
                  key={building.building_name}
                  building={building}
                  selected={building.building_name === currentBuilding?.building_name}
                  onChange={handleBuildingChange}
                />
              ))}
            </ScrollView>
          </MotiView>
        )}
      </AnimatePresence>

      <BuildingButton
        title={currentBuilding?.building_name ?? "Selecione um edifício"}
        open={false}
        onPress={() => setBuildingsVisible(true)}
      />

      <View className="mt-4">
        <SearchBar
          placeholder="Buscar sala"
          value={search}
          onChangeText={setSearch}
          onClear={() => setSearch("")}
        />
      </View>

      <View className="border-b pb-2 border-zinc-800 -mx-4 px-4">
        <ScrollView horizontal className="flex-row space-x-3 mt-3" showsHorizontalScrollIndicator={false}>
          <TouchableOpacity className={currentSpace.building_space_pk === defaultSpace.building_space_pk ? "border-b-2 border-amber-500" : ""} onPress={() => setCurrentSpace(defaultSpace)}>
            <Text className={`text-sm uppercase font-bold ${currentSpace.building_space_pk === defaultSpace.building_space_pk ? "text-amber-500" : "text-white"}`}>
              {defaultSpace.space_name}
            </Text>
          </TouchableOpacity>
          
          {filteredSpaces.map(space => (
            <TouchableOpacity
              key={space.building_space_pk}
              className={currentSpace.building_space_pk === space.building_space_pk ? "border-b-2 border-amber-500" : ""}
              onPress={() => setCurrentSpace(space)}
            >
              <Text
                className={`uppercase text-sm font-bold ${currentSpace.building_space_pk === space.building_space_pk ? "text-amber-500" : "text-white"}`}
              >
                {space.space_name}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      <ScrollView className="space-y-4" showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingVertical: 16 }}>
        {!searchRooms.length && <EmptyData icon="no-meeting-room" message="Nenhuma sala encontrada!" />}
        {searchRooms.map(room => {
          return (
            <RoomItem
              key={room.room_name}
              room={room}
              spaceName={room.space_name ?? currentSpace.space_name}
              buildings={currentBuilding ? [currentBuilding] : []}
            />
          );
        })}
      </ScrollView>
    </SafeAreaView>
  );
}
