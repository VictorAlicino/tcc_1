import { MaterialIcons } from "@expo/vector-icons";
import colors from "tailwindcss/colors";

interface IconProps {
  name: keyof typeof MaterialIcons.glyphMap;
  size?: number;
}

export function Icon({ name, size = 22 }: IconProps) {
  return <MaterialIcons name={name} size={size} color={colors.gray[100]} />;
}
