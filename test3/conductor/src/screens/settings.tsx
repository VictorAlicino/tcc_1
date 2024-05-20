import { TouchableOpacity } from "react-native";

import { Icon } from "@/components/icon";
import { SafeAreaView } from "@/components/safe-area-view";
import { Text } from "@/components/text";

export function Settings() {
  return (
    <SafeAreaView>
      <TouchableOpacity
        className="bg-zinc-800 flex-row items-center space-x-2 mt-4 p-4 rounded-full"
        activeOpacity={0.7}
      >
        <Icon name="person" size={24} />
        <Text className="text-xl font-500">Olá, Victor Alicino!</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}
