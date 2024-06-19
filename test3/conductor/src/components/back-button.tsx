import React from 'react';
import { StyleSheet, View, Text } from 'react-native';

interface CircleProps {
  size: number;
  text: string;
  color: string;
  fontSize: number;
}

const Circle: React.FC<CircleProps> = ({ size, text, color, fontSize }) => {
  const styles = StyleSheet.create({
    circle: {
      width: size,
      height: size,
      borderRadius: size / 2, // borderRadius should be half of the width/height to make it a perfect circle
      backgroundColor: color,
      justifyContent: "center", // centers the text vertically
      alignItems: "center", // centers the text horizontally
    },
    text: {
      color: "black", // or any color you prefer
      fontSize: fontSize, // use the fontSize prop for the text size
      fontWeight: "bold", // optional, if you want bold text
    },
  });

  return (
    <View style={styles.circle}>
      <Text style={styles.text}>{text}</Text>
    </View>
  );
};