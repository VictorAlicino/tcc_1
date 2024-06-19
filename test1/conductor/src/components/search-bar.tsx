import { useRef } from "react";
import { TextInput, TextInputProps, TouchableOpacity, View } from "react-native";
import colors from "tailwindcss/colors";

import { Icon } from "@/components/icon";

interface SearchBarProps extends TextInputProps {
  onClear?: () => void;
}

export function SearchBar({ onClear, ...props }: SearchBarProps) {
  const ref = useRef<TextInput>(null);

  function handleClear() {
    ref.current?.blur();
    onClear?.();
  }

  return (
    <View className="bg-zinc-800 p-2 flex-row space-x-2 items-center rounded-lg">
      <Icon name="search" />
      <TextInput
        ref={ref}
        className="font-400 text-zinc-100 text-base flex-1"
        placeholderTextColor={colors.zinc[100] + "70"}
        {...props}
      />
      {props.value && (
        <TouchableOpacity activeOpacity={0.7} onPress={handleClear}>
          <Icon name="close" />
        </TouchableOpacity>
      )}
    </View>
  );
}
