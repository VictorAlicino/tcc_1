import { TouchableOpacity, View, StyleSheet, ToastAndroid } from "react-native";
import React, { useState } from "react";
import { Overlay } from "react-native-elements";
import { Icon } from "@/components/icon";
import { SafeAreaView } from "@/components/safe-area-view";
import { Text } from "@/components/text";
import { SpaceItem } from "@/components/space-item";
import { Circle, type MaterialCommunityIconName, type MaterialIconName } from "@/components/circle";
import Spacer from "@/components/spacer";
import { StackItemProps } from "@/routes/protected-routes";
import { api } from "@/services/api";
import { HVACPayload } from "@/models/devices_models";

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

interface HVACData {
  power_state: string;
  temperature: number;
  mode: string;
  fan_speed: string;
}

export function OpusHVAC({ navigation, route } : StackItemProps<"HVACControl">) {

  const [isHVACOn, setIsHVACOn] = useState(false);
  const [temp, setTemp] = useState(24);
  const [mode, setMode] = useState(modes[0]);
  const [fanSpeed, setFanSpeed] = useState(fanSpeeds[0]);
  const [isLoaded, setIsLoaded] = useState(false);

  const bgColor = isHVACOn ? "#D5FBFF" : "white";
  const textHVAC = isHVACOn ? "Ligado" : "Desligado";

  // Call the API to get the current state of the HVAC
  async function getHVACState() {
    try{
      const response = await api.get<HVACPayload>(
        "/opus_server/" + 
        route.params.buildings[0].server_pk + 
        "/devices/" + 
        route.params.device.device_pk
      );
      //console.log(response.data);
      setIsHVACOn(response.data.power_state === "On");
      setTemp(response.data.temperature);
      setMode(modes.find((m) => m.name === response.data.mode) || modes[0]);
      setFanSpeed(fanSpeeds.find((f) => f.id === response.data.fan_speed) || fanSpeeds[0]);
    } catch (error) {
      console.error("Error fetching HVAC state:", error);
    }
  }

  async function setHVACState(payload: HVACData) {
    try {
      const response = await api.put(
        "/opus_server/" + 
        route.params.buildings[0].server_pk + 
        "/devices/" + 
        route.params.device.device_pk +
        "/set_state",
        payload
      ).catch((error) => {
        // if error 400
        switch (error.response.status) {
          case 400:
          case 401:
          case 500:
            ToastAndroid.show("Você não tem mais acesso a esse dispositivo", ToastAndroid.SHORT);
            break;
          default:
            console.error("Error setting HVAC state:", error);
            break;
        }
        handleGoBack();
      });
    }
    catch (error) {
      console.error("Error setting HVAC state:", error);
    }
  }
  
  // Fetch the HVAC state when the component is loaded
  useState(() => {
    getHVACState();
    setIsLoaded(true);
  }
  );

  function handleSwitchMode() {
    const index = modes.indexOf(mode);
    if (index === modes.length - 1) {
      setMode(modes[0]);
      setHVACState(
        {
          power_state: isHVACOn ? "On" : "Off",
          temperature: temp,
          mode: modes[0].name,
          fan_speed: fanSpeed.id ? fanSpeed.id : "Auto"
        }
      )
    } else {
      setMode(modes[index + 1]);
      setHVACState(
        {
          power_state: isHVACOn ? "On" : "Off",
          temperature: temp,
          mode: modes[index + 1].name,
          fan_speed: fanSpeed.id ? fanSpeed.id : "Auto"
        }
      )
    }
  }

  function handleSwitchFanSpeed() {
    const index = fanSpeeds.indexOf(fanSpeed);
    if (index === fanSpeeds.length - 1) {
      setFanSpeed(fanSpeeds[0]);
      setHVACState(
        {
          power_state: isHVACOn ? "On" : "Off",
          temperature: temp,
          mode: mode.name,
          fan_speed: fanSpeeds[0].name
        }
      );
    } else {
      setFanSpeed(fanSpeeds[index + 1]);
      setHVACState(
        {
          power_state: isHVACOn ? "On" : "Off",
          temperature: temp,
          mode: mode.name,
          fan_speed: fanSpeeds[index + 1].name
        }
      );
    }
  }  
  
  const tempUp = () => {
    if (temp < 30) {
      const new_temp = temp + 1;
      setTemp(new_temp);
      setHVACState({
        power_state: isHVACOn ? "On" : "Off",
        temperature: new_temp,
        mode: mode.name,
        fan_speed: fanSpeed.id ? fanSpeed.id : "Auto"
      });
    }
  };
  
  const tempDown = () => {
    if (temp > 16) {
      const new_temp = temp - 1;
      setTemp(new_temp);
      setHVACState({
        power_state: isHVACOn ? "On" : "Off",
        temperature: new_temp,
        mode: mode.name,
        fan_speed: fanSpeed.id ? fanSpeed.id : "Auto"
      });
    }
  };

  const handleToggleSwitch = () => {
    setIsHVACOn((prev) => {
      const newState = !prev;
      setHVACState({
        power_state: newState ? "On" : "Off",
        temperature: temp,
        mode: mode.name,
        fan_speed: fanSpeed.id ? fanSpeed.id : "Auto"
      });
      return newState;
    });
  }

  const handleGoBack = () => {
    navigation.goBack();
  }

  // Print DeviceItem coming from previous screen
  //console.log(route.params);

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
          <TouchableOpacity onPress={handleGoBack}>
              <Icon name="arrow-back-ios" size={30} />
          </TouchableOpacity>
          <View className="flex-1 items-center">
              <Text className="text-xl font-500">Ar Condicionado</Text>
              <Text style={{fontSize:15}}>Sala 01</Text>
          </View>
          <TouchableOpacity >
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
          
          <TouchableOpacity onPress={() => handleToggleSwitch() } style={{padding: 15}}>
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
            <Text style={{ fontSize: 15 }}>{fanSpeed.id ? fanSpeed.id : "Auto"}</Text>
          </TouchableOpacity>
        </View>
        <Spacer y={30}/>
      </View>
    </SafeAreaView>
  );
}
