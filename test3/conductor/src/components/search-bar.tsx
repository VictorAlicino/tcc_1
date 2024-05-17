import { TextInput, TextInputProps, View } from "react-native";
import colors from "tailwindcss/colors"

import { Icon } from "@/components/icon";

interface SearchBarProps extends TextInputProps {
}

export function SearchBar({ ...props }: SearchBarProps) {
  return (
    <View className="bg-gray-800 py-2 px-4 flex-row space-x-2 items-center rounded-lg">
      <Icon name="search" />
      <TextInput
        className="font-400 text-gray-100 text-base"
        placeholderTextColor={colors.gray[100] + "70"}
        {...props}
      />      
    </View>
  );
}
