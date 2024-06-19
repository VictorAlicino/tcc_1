import { Text as RNText, TextProps } from "react-native";

export function Text(props: TextProps) {
  return <RNText className="font-400 text-zinc-100 text-base" {...props} />;
}
