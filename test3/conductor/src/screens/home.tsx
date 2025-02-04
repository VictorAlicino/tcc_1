import { AnimatePresence, MotiView } from "moti";
import { useEffect, useState } from "react";
import { ScrollView, View } from "react-native";
import colors from "tailwindcss/colors";
import { api } from "@/services/api";

import { BuildingButton } from "@/components/building-button";
import { BuildingItem } from "@/components/building-item";
import { EmptyData } from "@/components/empty-data";
import { RoomItem } from "@/components/room-item";
import { BuildingData, DeviceData, RoomData, SpaceData} from "@/models/opus-models";
import { SafeAreaView, statusBarHeight } from "@/components/safe-area-view";
import { SearchBar } from "@/components/search-bar";
import { SpaceItem } from "@/components/space-item";

const buildings: BuildingData[] = [
  {
    id: "1",
    name: "Bloco 1",
    role: "ADMIN",
  },
  {
    id: "2",
    name: "Bloco 2",
    role: "ADMIN",
  },
  {
    id: "3",
    name: "Bloco 3",
    role: "USER",
  },
  {
    id: "4",
    name: "Bloco 4",
    role: "USER",
  },
  {
    id: "5",
    name: "Bloco 5",
    role: "USER",
  },
  {
    id: "6",
    name: "Bloco 6",
    role: "ADMIN",
  },
];

export const spaces: SpaceData[] = [
  {
    id: "1234",
    name: "Espaço 01",
    buildingId: "1",
  },
  {
    id: "1233",
    name: "Espaço 02",
    buildingId: "1",
  },
  {
    id: "1232",
    name: "Espaço 03",
    buildingId: "2",
  },
  {
    id: "1231",
    name: "Espaço 04",
    buildingId: "2",
  },
];

export const rooms: RoomData[] = [
  {
    id: "1",
    name: "Sala 01",
    spaceId: "1234",
    devicesCount: 1,
  },
  {
    id: "2",
    name: "Sala 02",
    spaceId: "1234",
    devicesCount: 3,
  },
  {
    id: "3",
    name: "Sala 03",
    spaceId: "1234",
    devicesCount: 5,
  },
  {
    id: "4",
    name: "Sala 04",
    spaceId: "1233",
    devicesCount: 1,
  },
  {
    id: "5",
    name: "Sala 05",
    spaceId: "1232",
    devicesCount: 1,
  },
  {
    id: "50",
    name: "Sala 05",
    spaceId: "1232",
    devicesCount: 6,
  },
  {
    id: "51",
    name: "Sala 51",
    spaceId: "1231",
    devicesCount: 2,
  },
  {
    id: "52",
    name: "Sala 52",
    spaceId: "1231",
    devicesCount: 0,
  },
  {
    id: "53",
    name: "Sala 53",
    spaceId: "1232",
    devicesCount: 1,
  },
];



let availableBuildings: BuildingData[] = [];
let availableSpaces: SpaceData[] = [];
let availableRooms: RoomData[] = [];
let availableDevices: DeviceData[] = [];

async function getBuildings() {
  let opusResponse;
  api.get("/users/opus_server/dump_all_servers_info")
    .then(response => {
      opusResponse = response.data;
      console.log(response.data);
      console.log(response.data['opus-server-5be2']);
    })
    .catch(error => {
      console.error(error);
      return [];
    });

  //if(opusResponse) {
  //  const buildingData = Object.values(opusResponse)[0];
  //  if(buildingData && buildingData.buildings) {
  //    availableBuildings = buildingData.buildings.map(building => ({
  //      pk: building.building_pk,
  //      name: building.building_name,
  //      role: building.building_role,
  //    })
  //  }
  //}
}

export function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState(null);

  useEffect(() => {
    setIsLoading(true);

    api.get("/users/opus_server/dump_all_servers_info")
      .then(response => {
        setData(response.data);
        setIsLoading(false);
        for (const server in response.data) {
          console.log("--------------------------");
          console.log("Buildings on server: " + server);
          if(response.data[server]){
            for (const building in response.data[server].buildings) {
              console.log("\t" + response.data[server].buildings[building].building_name);
              for (const spaces in response.data[server].buildings[building].spaces){
                console.log("\t\t" + response.data[server].buildings[building].spaces[spaces].space_name);
                for (const rooms in response.data[server].buildings[building].spaces[spaces].rooms){
                  console.log("\t\t\t" + response.data[server].buildings[building].spaces[spaces].rooms[rooms].room_name);
                  for (const devices in response.data[server].buildings[building].spaces[spaces].rooms[rooms].devices){
                    console.log("\t\t\t\t" + response.data[server].buildings[building].spaces[spaces].rooms[rooms].devices[devices].device_name);
                  }
                }
              }
            }
          }
          else{
            console.log("\tNo buildings found");
          }
        };
      })
      .catch(error => {
        console.error(error);
        setIsLoading(false);
      });
  }, []);

  const [buildingsVisible, setBuildingsVisible] = useState(false);
  const [search, setSearch] = useState("");
  const [searchBuilding, setSearchBuilding] = useState("");




  const [currentBuilding, setCurrentBuilding] = useState<BuildingData>(buildings[0]);

  const defaultSpace = {
    id: "ALL",
    name: "Todos",
    buildingId: currentBuilding.id,
  };

  const [currentSpace, setCurrentSpace] = useState<SpaceData>(defaultSpace);

  const filteredSpaces = spaces.filter((space) => {
    return space.buildingId === currentBuilding.id;
  });

  const filteredRooms = rooms.filter((room) => {
    if (currentSpace.id === "ALL") {
      return filteredSpaces.some((space) => space.id === room.spaceId);
    }

    return room.spaceId === currentSpace.id;
  });

  const searchRooms = filteredRooms.filter((room) => {
    return room.name.toLowerCase().includes(search.toLowerCase());
  });

  const searchBuildings = buildings.filter((building) => {
    return building.name.toLowerCase().includes(searchBuilding.toLowerCase());
  });

  function handleBuildingChange(building: BuildingData) {
    setCurrentBuilding(building);
    setBuildingsVisible(false);
  }

  useEffect(() => {
    setCurrentSpace(defaultSpace);
  }, [currentBuilding]);

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
            <BuildingButton title={currentBuilding.name} open={true} onPress={() => setBuildingsVisible(false)} />

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
                <EmptyData icon="apartment" message="Você não possui edíficios com esse filtro!" />
              )}

              {searchBuildings.map((building) => (
                <BuildingItem
                  key={building.id}
                  building={building}
                  selected={building.id === currentBuilding.id}
                  onChange={handleBuildingChange}
                />
              ))}
            </ScrollView>
          </MotiView>
        )}
      </AnimatePresence>

      <BuildingButton title={currentBuilding.name} open={false} onPress={() => setBuildingsVisible(true)} />

      <View className="mt-4">
        <SearchBar
          placeholder="Buscar sala em espaços"
          value={search}
          onChangeText={setSearch}
          onClear={() => setSearch("")}
        />
      </View>

      <View className="border-b pb-2 border-zinc-800 -mx-4 px-4">
        <ScrollView
          className="mt-4 -mx-4"
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={{
            gap: 14,
            paddingHorizontal: 16,
          }}
        >
          <SpaceItem
            space={defaultSpace}
            selected={defaultSpace.id === currentSpace.id}
            onPress={() => setCurrentSpace(defaultSpace)}
          />

          {filteredSpaces.map((space) => (
            <SpaceItem
              key={space.id}
              space={space}
              selected={space.id === currentSpace.id}
              onPress={() => setCurrentSpace(space)}
            />
          ))}
        </ScrollView>
      </View>

      <ScrollView
        className="space-y-4"
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingVertical: 16 }}
      >
        {!searchRooms.length && <EmptyData icon="no-meeting-room" message="Você não possui salas nesse espaço!" />}

        {searchRooms.map((room) => {
          const space = spaces.find((space) => space.id === room.spaceId);
          return <RoomItem key={room.id} room={room} spaceName={space?.name || currentSpace.name} />;
        })}
      </ScrollView>
    </SafeAreaView>
  );
}
