import { SafeAreaView as RNSafeAreaView, StatusBar, ViewProps } from "react-native";

export const statusBarHeight = StatusBar.currentHeight || 0;

const extraPadding = statusBarHeight < 30 ? 16 : 0;

export function SafeAreaView(props: ViewProps) {
  return (
    <RNSafeAreaView
      className="flex-1 bg-zinc-900 px-4"
      style={{ paddingTop: statusBarHeight + extraPadding }}
      {...props}
    />
  );
}
