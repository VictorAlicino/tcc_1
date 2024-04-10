import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

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
                  Image.asset("assets/images/opus_logo.png", height: 150),
                  Container(
                    margin: const EdgeInsets.only(top: 150),
                    child: ElevatedButton(
                        onPressed: () => null,
                        child: const Text("Login",
                            style: TextStyle(fontSize: 20))),
                  ),
                  Container(
                    margin: const EdgeInsets.only(top: 25),
                    child: ElevatedButton(
                        onPressed: () => null,
                        child: const Text("Register",
                            style: TextStyle(fontSize: 20))),
                  )
                ])));
  }
}
