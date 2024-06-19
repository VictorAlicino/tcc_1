import { TouchableOpacity, View, StyleSheet } from "react-native";
import React, { useState } from "react";
import { Overlay } from "react-native-elements";
import { Icon } from "@/components/icon";
import { SafeAreaView } from "@/components/safe-area-view";
import { Text } from "@/components/text";
import { SpaceItem } from "@/components/space-item";
import { Circle, type MaterialCommunityIconName, type MaterialIconName } from "@/components/circle";
import Spacer from "@/components/spacer";

interface HVACMode {
  id?: string;
  name: string;
  icon: MaterialCommunityIconName | MaterialIconName;
}

const modes: HVACMode[] = [
  {
    name: "Auto",
    icon: "thermostat-auto"
  }, {
    name: "Cool",
    icon: "snowflake"
  }, {
    name: "Heat",
    icon: "fire"
  }, {
    name: "Dry",
    icon: "water"
  }, {
    name: "Fan",
    icon: "fan"
  },
];

const fanSpeeds: HVACMode[] = [
  {
    id: "Auto",
    name: "Auto",
    icon: "fan-auto"
  },
  {
    id: "Min",
    name: "Mín.",
    icon: "fan-minus"
  },
  {
    id: "Low",
    name: "Lento",
    icon: "fan-speed-1"
  },
  {
    id: "Med",
    name: "Méd.",
    icon: "fan-speed-2"
  },
  {
    id: "High",
    name: "Rápido",
    icon: "fan-speed-3"
  },
  {
    id: "Max",
    name: "Máx.",
    icon: "fan-plus"
  },
]

export function OpusHVAC() {

  const [isHVACOn, setIsHVACOn] = useState(false);
  const [temp, setTemp] = useState(24);
  const [mode, setMode] = useState(modes[0]);
  const [fanSpeed, setFanSpeed] = useState(fanSpeeds[0]);

  const bgColor = isHVACOn ? "#D5FBFF" : "white";
  const textHVAC = isHVACOn ? "Ligado" : "Desligado";

  function handleSwitchMode() {
    const index = modes.indexOf(mode);
    if (index === modes.length - 1) {
      setMode(modes[0]);
    } else {
      setMode(modes[index + 1]);
    }
  }

  function handleSwitchFanSpeed() {
    const index = fanSpeeds.indexOf(fanSpeed);
    if (index === fanSpeeds.length - 1) {
      setFanSpeed(fanSpeeds[0]);
    } else {
      setFanSpeed(fanSpeeds[index + 1]);
    }
  }  
  
  const tempUp = () => {
    if(temp < 30){
      setTemp(temp + 1);
    }
  }

  const tempDown = () => {
    if(temp > 16){
      setTemp(temp - 1);
    }
  }

  return (
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
              <Text className="text-xl font-500">Ar Condicionado</Text>
              <Text style={{fontSize:15}}>Sala 01</Text>
          </View>
          <TouchableOpacity>
              <Icon name="report" size={30} />
          </TouchableOpacity>
        </View>
        <View className="flex-1 items-center justify-center">
          <Circle size={200} text={temp + "ºC"} color={bgColor} fontSize={50} />
          <Spacer y={10}/>
          <Text className="text-xl font-500">{textHVAC}</Text>
        </View>

        <View style={{
          flexDirection:'row',
          justifyContent:'space-evenly',
          alignItems:'center'
        }}>
          <TouchableOpacity onPress={() => tempDown()}>
            <Circle 
              size={70}
              color="#5A25D9"
              fontSize={20}
              icon={{name:"thermometer-chevron-down", size:30, color:"white"}}
              />
          </TouchableOpacity>
          <Spacer />
          <TouchableOpacity onPress={() => tempUp()}>
            <Circle 
              size={70}
              color="#5A25D9"
              fontSize={20}
              icon={{ name: "thermometer-chevron-up", size: 30, color: "white" }}
            />
          </TouchableOpacity>
        </View>
        
        <Spacer y={30}/>

        <View className="flex-row justify-evenly items-center">
          <TouchableOpacity className="items-center justify-center" onPress={handleSwitchMode}>
            <Circle 
              size={65}
              color="#5A25D9"
              fontSize={20}
              icon={{ name: mode.icon, size: 30, color: "white" }}
            />
            <Text style={{ fontSize: 15 }}>{mode.name}</Text>
          </TouchableOpacity>
          
          <TouchableOpacity onPress={() => setIsHVACOn(!isHVACOn)} style={{padding: 15}}>
            <Circle 
              size={115}
              color="#2E3844"
              fontSize={20}
              icon={{ name: "power", size: 70, color: "white" }}
              />
          </TouchableOpacity>

          <TouchableOpacity className="items-center justify-center" onPress={handleSwitchFanSpeed}>
              <Circle 
                size={65}
                color="#5A25D9"
                fontSize={20}
                icon={{ name: fanSpeed.icon, size: 30, color: "white" }}
              />
            <Text style={{ fontSize: 15 }}>{fanSpeed.name}</Text>
          </TouchableOpacity>
        </View>
        <Spacer y={30}/>
      </View>
    </SafeAreaView>
  );
}
