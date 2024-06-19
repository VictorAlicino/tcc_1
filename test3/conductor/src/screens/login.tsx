import { View, Image, TouchableOpacity } from "react-native";
import { Text } from "@/components/text";
import { Icon } from "@/components/icon";
import { SafeAreaView } from "@/components/safe-area-view";
import { api } from "@/services/api";
import { useAuthentication } from "@/contexts/authentication-context";

export function Login() {
  const { googleSignIn } = useAuthentication();

  return (
    <SafeAreaView>
        <View className="flex-1 items-center justify-center bg-zinc-900">
        <View style={{flex:4,flexDirection:"row",justifyContent:'space-between',padding:0}}>
            </View>
            <View className="items-center justify-center">
                <Image 
                    source={require("../../assets/opus-conductor.png")} 
                    style={{ width: 300, height: 200 }}
                    resizeMethod="scale"
                    resizeMode="center"
                />
            </View>
            <View style={{flex:2,flexDirection:"row",justifyContent:'space-between',padding:0}}>
            </View>
            <View>
                <TouchableOpacity
                    className="bg-slate-600 flex-row items-center space-x-2 mt-4 p-4 rounded-full"
                    activeOpacity={0.7}
                    onPress={googleSignIn}
                >
                    <Icon name="google" size={30} />
                    <Text className="text-base font-500 px-4">Entrar com o Google</Text>

                </TouchableOpacity>
            </View>
            <View style={{flex:2,flexDirection:"row",justifyContent:'space-between',padding:0}}>
            </View>
        </View>
    </SafeAreaView>
  );
}
