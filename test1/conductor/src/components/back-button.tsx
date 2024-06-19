import { TouchableOpacity, View } from "react-native";

import { Icon } from "@/components/icon";
import { statusBarHeight } from "@/components/safe-area-view";

export function BackButton() {
  return (
    <View
      className="bg-zinc-800 -mx-4 p-4"
      style={{
        marginTop: -statusBarHeight,
        paddingTop: statusBarHeight,
      }}
    >
      <TouchableOpacity className="bg-zinc-900 p-2 rounded-full">
        <Icon name="chevron-left" />
      </TouchableOpacity>
    </View>
  );
}
