import { MaterialIcons, FontAwesome } from "@expo/vector-icons";
import colors from "tailwindcss/colors";

export type MaterialIconName = keyof typeof MaterialIcons.glyphMap;
export type FontAwesomeIconName = keyof typeof FontAwesome.glyphMap;

interface IconProps {
  name: MaterialIconName | FontAwesomeIconName;
  size?: number;
  color?: string;
}

export function Icon({ name, size = 22, color = colors.zinc[100] }: IconProps) {
  if (name in MaterialIcons.glyphMap) {
    return <MaterialIcons name={name as MaterialIconName} size={size} color={color} />;
  }
  return <FontAwesome name={name as FontAwesomeIconName} size={size} color={color} />;
}
