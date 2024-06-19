import { SafeAreaView } from "@/components/safe-area-view";
import { View } from "react-native";
import { Icon } from "@/components/icon";
import { Text } from "@/components/text";
import { TouchableOpacity } from "react-native-gesture-handler";
import { Circle } from "@/components/circle";
import Spacer from "@/components/spacer";
import { useEffect, useState } from "react";

export function OpusLight(){

  const [isLightOn, setIsLightOn] = useState(false);

  let bgColog = isLightOn ? "yellow" : "white";
  let textLight = isLightOn ? "Ligado" : "Desligado";

  return(
    <SafeAreaView>
      <View style={{
          flexDirection:'column',
          flex:1,
          padding:10
      }}>

        <View style={{
          flexDirection:'row',
          justifyContent:'space-evenly',
          alignItems:'center',
          paddingTop:15
        }}>
          <TouchableOpacity>
              <Icon name="arrow-back-ios" size={30} />
          </TouchableOpacity>
          <View className="flex-1 items-center justify-center">
              <Text className="text-xl font-500">Luz 1</Text>
              <Text style={{fontSize:15}}>Sala 01</Text>
          </View>
          <TouchableOpacity>
              <Icon name="report" size={30} />
          </TouchableOpacity>
        </View>

        <View className="flex-1 items-center justify-center">
          <TouchableOpacity onPress={() => setIsLightOn(!isLightOn)}>
            <Circle size={200} color={bgColog} icon={{name: "lightbulb-outline", color: "black", size: 80}} />
          </TouchableOpacity>
          <Spacer height={"5%"} />
          <Text className="text-xl font-500">{textLight}</Text>
        </View>
        <Spacer height={"25%"} />
      </View>
    </SafeAreaView>
  );
}