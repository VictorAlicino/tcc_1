import { clsx } from "clsx";
import { TouchableOpacity, TouchableOpacityProps } from "react-native";
import { SpaceData } from "@/models/opus-models";

import { Text } from "@/components/text";

export interface SpaceItemProps extends TouchableOpacityProps {
  space: SpaceData;
  selected: boolean;
}

export function SpaceItem({ space, selected, ...props }: SpaceItemProps) {
  return (
    <TouchableOpacity className="p-1" activeOpacity={0.7} {...props}>
      <Text
        className={clsx(
          "font-500 uppercase",
          selected && "text-amber-500 border-b-[3px] border-amber-500 md:border-b-2"
        )}
      >
        {space.space_name}
      </Text>
    </TouchableOpacity>
  );
}
