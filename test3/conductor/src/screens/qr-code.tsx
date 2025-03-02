import { SafeAreaView } from "@/components/safe-area-view";
import { Text } from "@/components/text";
import { CameraView, useCameraPermissions } from 'expo-camera';
import { View, useWindowDimensions, Linking } from "react-native";
import { useCallback, useEffect, useState } from "react";
import { api } from "@/services/api";
import { guestAPIResponse } from "@/models/conductor_models";
import { OpusHVAC } from "./opus_hvac";
import { useNavigation } from "@react-navigation/native";
import { StackItemProps } from "@/routes/protected-routes";
import { opusDevices, opusBuilding } from "@/models/conductor_models";

export function QRCode() {
  const navigation = useNavigation<StackItemProps["navigation"]>();
  const [permission, requestPermission] = useCameraPermissions();
  const [scanned, setScanned] = useState<Date>();
  const [guestAccess, setGuestAccess] = useState<guestAPIResponse | null>(null);
  const [available, setAvailable] = useState(false);

  function handleScanQR(data: string) {
    if (scanned !== undefined && new Date().getTime() - scanned.getTime() < 10000) return;
    setScanned(new Date());
    api.get<guestAPIResponse>(`opus_server/guest_access/${data}`).then((response) => {
      setGuestAccess(response.data);
      setAvailable(true);
      console.log(response.data);
    }
    ).catch((error) => {
      console.log(error);
    }
    );
    setAvailable(true);
  }

  useEffect(() => {
    if (!permission?.granted){
      requestPermission();
    }
  }, []);

  useEffect(() => {
    //console.log("Oi");
    if (available && guestAccess && guestAccess.grant_until < new Date()) {
      console.log("oi2");
      const device: opusDevices = guestAccess.device;
      const building: opusBuilding = {
        server_pk: guestAccess.server_id,
        building_pk: "",
        building_name: "",
        security_level: "",
        spaces: [],
      };

      if (guestAccess.device.device_type === "HVAC") {
        navigation.navigate("HVACControl", { device, buildings: [building] });
      } else {
        // Se o tipo não for reconhecido, reseta o estado
        setAvailable(false);
      }
    }
  }, [available, guestAccess]);

  return (
    <SafeAreaView className="flex-1 justify-center">
      <Text className="text-left text-3xl font-700 mb-1">Olá!</Text>
      <Text className="text-left text-lg font-500 mb-4">
        Escaneie o QR Code da Sala para acessar o controle do dispositivo
      </Text>
      <View className="rounded-xl overflow-hidden border-2 border-amber-500">
        <CameraView
          style={{ height: 350 }}
          barcodeScannerSettings={{ barcodeTypes: ["qr"] }}
          onBarcodeScanned={(result) => handleScanQR(result.data)}
        />
      </View>
    </SafeAreaView>
  );
}
