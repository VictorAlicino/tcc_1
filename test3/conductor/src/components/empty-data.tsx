import { View } from "react-native";

import { Icon, MaterialIconName } from "@/components/icon";
import { Text } from "@/components/text";

interface EmptyDataProps {
  icon: MaterialIconName;
  message: string;
}

export function EmptyData({ icon, message }: EmptyDataProps) {
  return (
    <View className="space-y-2 items-center">
      <Icon name={icon} size={24} />
      <Text className="opacity-70 max-w-[50%] text-center">{message}</Text>
    </View>
  );
}
