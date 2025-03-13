import { TouchableOpacity, View, Image } from "react-native";
import { Icon } from "@/components/icon";
import { SafeAreaView } from "@/components/safe-area-view";
import { Text } from "@/components/text";
import { SpaceItem } from "@/components/space-item";
import { useAuthentication } from "@/contexts/authentication-context";

export function Settings() {
  const { getCurrentUser, signOut } = useAuthentication();
  const user = getCurrentUser();

  return (
    <SafeAreaView>
      <View style={{
        flexDirection:'column',
        flex:1,
      }}>
        <TouchableOpacity
          className="bg-zinc-800 flex-row items-center space-x-2 mt-5 p-2 rounded-full"
          activeOpacity={0.7}
        >
          <Image
            style={{width: 45, height: 45, borderRadius: 50}}
            source={{uri: user?.photo ?? ''}}
          />
          <Text className="text-xl font-700 px-2">Olá, {user?.name}!</Text>
        </TouchableOpacity>

        <View style={{flex:2,flexDirection:"row",justifyContent:'space-between',padding:0}}>
        </View>

        <TouchableOpacity
          className="bg-red-800 flex-row space-x-2 p-3 rounded-t-xl items-center"
          onPress={signOut} // Mova onPress para esse TouchableOpacity
          activeOpacity={0.7}
        >
          <Icon name="logout" size={24} />
          <Text className="text-xl font-400">Sair</Text>
        </TouchableOpacity>

      </View>
    </SafeAreaView>
  );
}
