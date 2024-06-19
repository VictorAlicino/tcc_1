import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { MaterialIcons, MaterialCommunityIcons } from "@expo/vector-icons";
import colors from "tailwindcss/colors";

// Componente Icon
export type MaterialIconName = keyof typeof MaterialIcons.glyphMap;
export type MaterialCommunityIconName = keyof typeof MaterialCommunityIcons.glyphMap;

interface IconProps {
  name: MaterialIconName;
  size?: number;
  color?: string;
}

export function Icon({ name, size = 22, color = colors.zinc[100] }: IconProps) {
  if (name in MaterialCommunityIcons.glyphMap) {
    return <MaterialCommunityIcons name={name as MaterialCommunityIconName} size={size} color={color} />;
  }
  return <MaterialIcons name={name} size={size} color={color} />;
}

// Componente Circle
interface CircleProps {
  size: number;
  text?: string;
  color: string;
  fontSize?: number;
  icon?: {
    name: MaterialIconName | MaterialCommunityIconName;
    size?: number;
    color?: string;
  };
}

const Circle: React.FC<CircleProps> = ({ size, text, color, fontSize, icon }) => {
  const styles = StyleSheet.create({
    circle: {
      width: size,
      height: size,
      borderRadius: size / 2, // borderRadius should be half of the width/height to make it a perfect circle
      backgroundColor: color,
      justifyContent: "center", // centers the content vertically
      alignItems: "center", // centers the content horizontally
    },
    text: {
      color: "black", // or any color you prefer
      fontSize: fontSize, // use the fontSize prop for the text size
      fontWeight: "bold", // optional, if you want bold text
    },
  });

  return (
    <View style={styles.circle}>
      {icon ? (
        <Icon name={icon.name} size={icon.size} color={icon.color} />
      ) : (
        <Text style={styles.text}>{text}</Text>
      )}
    </View>
  );
};


export { Circle };