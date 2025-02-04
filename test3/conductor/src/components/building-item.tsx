import { clsx } from "clsx";
import { TouchableOpacity, TouchableOpacityProps, View } from "react-native";
import colors from "tailwindcss/colors";
import { BuildingData } from "@/models/opus-models";

import { Icon } from "@/components/icon";
import { Text } from "@/components/text";

interface BuildingItemProps extends TouchableOpacityProps {
  building: BuildingData;
  selected: boolean;
  onChange: (building: BuildingData) => void;
}

export function BuildingItem({ building, selected, onChange, ...props }: BuildingItemProps) {
  const isAdmin = building.role === "ADMIN";

  return (
    <TouchableOpacity
      className={clsx(
        "bg-zinc-800 rounded-xl p-4 flex-row items-center justify-between border border-transparent",
        selected && "border-amber-500 bg-amber-500/5"
      )}
      activeOpacity={0.7}
      onPress={() => onChange(building)}
      {...props}
    >
      <View className="flex-row items-center space-x-5">
        <Icon name="apartment" size={36} />
        <Text className="text-xl font-700">{building.name}</Text>
      </View>
      <View className="items-center space-y-1">
        <Icon name="badge" color={isAdmin ? colors.amber[500] + "90" : colors.green[500] + "90"} />
        <Text className={clsx("text-xs text-green-500/60", isAdmin && "text-amber-500/60")}>
          {isAdmin ? "Admin" : "Usuário"}
        </Text>
      </View>
    </TouchableOpacity>
  );
}
