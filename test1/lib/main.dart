import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
            backgroundColor: const Color.fromARGB(255, 26, 24, 36),
            body: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Spacer(),
                  SvgPicture.asset("assets/images/opus_logo.svg"),
                  Spacer(),
                  ButtonTheme(
                    minWidth: 30,
                    height: 250,
                    child: ElevatedButton(
                        onPressed: () => null,
                        child: const Text("Login with Google",
                            style: TextStyle(fontSize: 20))),
                  ),
                  Container(
                    margin: const EdgeInsets.only(top: 25),
                    child: ElevatedButton(
                        onPressed: () => null,
                        child: const Text("Login with Microsoft",
                            style: TextStyle(fontSize: 20))),
                  ),
                  Spacer()
                ])));
  }
}
