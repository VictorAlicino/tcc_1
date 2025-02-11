import { TouchableOpacity, TouchableOpacityProps, View } from "react-native";
import { DeviceData } from "@/models/opus-models";
import { Icon } from "@/components/icon";
import { Text } from "@/components/text";

interface DeviceItemProps extends TouchableOpacityProps {
  device: DeviceData;
}

function getDeviceIcon(deviceType: string) {
    switch (deviceType) {
        case "HVAC":
            return "hvac";
        case "LIGHT":
            return "lightbulb";
    }
}

export function DeviceItem({ device, ...props }: DeviceItemProps) {
  return (
    <TouchableOpacity
      className="bg-zinc-800 rounded-xl p-4 items-center justify-center"
      activeOpacity={0.7}
      accessibilityLabel={`Detalhes do dispositivo ${device.device_name}`}
      {...props}
    >
      <Icon name={getDeviceIcon(device.device_type) || "devices"} size={36} />
      
      <Text className="text-center text-sm font-700 mt-2" numberOfLines={1}>
        {device.device_name}
      </Text>
    </TouchableOpacity>
  );
}