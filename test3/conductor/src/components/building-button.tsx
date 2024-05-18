import { TouchableOpacity, TouchableOpacityProps } from "react-native";

import { Icon } from "@/components/icon";
import { Text } from "@/components/text";

interface BuildingButtonProps extends TouchableOpacityProps {
  title: string;
  open: boolean;
}

export function BuildingButton({ title, open, ...props }: BuildingButtonProps) {
  return (
    <TouchableOpacity className="flex-row space-x-2 items-center self-center px-4" activeOpacity={0.7} {...props}>
      <Text className="font-500 text-lg">{title}</Text>
      <Icon name={open ? "arrow-drop-up" : "arrow-drop-down"} size={32} />
    </TouchableOpacity>
  );
}
