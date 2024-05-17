import { SafeAreaView as RNSafeAreaView, ViewProps, StatusBar } from "react-native"

const statusBarHeight = StatusBar.currentHeight || 0;

export function SafeAreaView(props: ViewProps) {
  return <RNSafeAreaView 
    className="flex-1 bg-gray-900 px-4"
    style={{ paddingTop: statusBarHeight + 24 }} 
    {...props} 
  />;
}
