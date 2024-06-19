import { MaterialIcons } from "@expo/vector-icons";
import colors from "tailwindcss/colors";

export type MaterialIconName = keyof typeof MaterialIcons.glyphMap;

interface IconProps {
  name: MaterialIconName;
  size?: number;
  color?: string;
}

export function Icon({ name, size = 22, color = colors.zinc[100] }: IconProps) {
  return <MaterialIcons name={name} size={size} color={color} />;
}
