import { ActivityIndicator, View, Image, useWindowDimensions } from "react-native";
import colors from "tailwindcss/colors";

export function Loading() {
  const{width} = useWindowDimensions();

  return (
    <View className="h-full items-center justify-center px-4 bg-zinc-900">
        <Image
          source={require("../../assets/opus-conductor-2.png")}
          style={{width, aspectRatio: 0.8}}
          resizeMode="center"
        />
        <ActivityIndicator size={50} color={colors.zinc[100]} />
    </View>
  );
}