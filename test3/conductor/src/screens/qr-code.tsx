import { SafeAreaView } from "@/components/safe-area-view";
import { Text } from "@/components/text";
import { CameraView, useCameraPermissions } from 'expo-camera';
import { View, useWindowDimensions, Linking } from "react-native";
import { useEffect } from "react";

export function QRCode() {
  const [permission, requestPermission] = useCameraPermissions();

  function handleScanQR(data: string) {
    // Linking.openURL("");
    alert(data);
  }
  
  useEffect(() => {
    if (!permission?.granted){
      requestPermission();
    }
  }, []);

  return (
    <SafeAreaView className="flex-1 justify-center">
      <Text className="text-left text-3xl font-700 mb-1">Olá!</Text>
      <Text className="text-left text-lg font-500 mb-4">
        Escaneie o QR Code da Sala para adicioná-la ao seu perfil
      </Text>
      <View className="rounded-xl overflow-hidden border-2 border-amber-500">
        <CameraView
          style={{
            height: 350,
          }}
          barcodeScannerSettings={{
            barcodeTypes: ["qr"],
          }}
          onBarcodeScanned={(result) => handleScanQR(result.data)}
        />
      </View>
    </SafeAreaView>
  );
}
