import 'package:flutter/material.dart';
import 'package:test1/main.dart';
//import 'package:flutter_svg/flutter_svg.dart';

var corBotao = const Color(0xFFD9AC25);

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
            backgroundColor: const Color.fromARGB(255, 26, 24, 36),
            body: Center(
              child: Container(
                padding: const EdgeInsets.all(15),
                child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      SizedBox(height: MediaQuery.of(context).size.height * 0.25),
                      //SvgPicture.asset("assets/images/opus_logo.svg"),
                      SizedBox(
                        width: MediaQuery.of(context).size.height * 0.3,
                        height: MediaQuery.of(context).size.height * 0.3,
                        child: Image.asset("assets/images/opus_logo.png")
                        ),
                      SizedBox(height: MediaQuery.of(context).size.height * 0.15),
                      ElevatedButton.icon(
                        onPressed: () {}, 
                        icon: const Icon(Icons.email), 
                        label: const Text(
                          "Login with Google   ",
                            style: TextStyle(
                            fontFamily: 'Roboto',
                            fontSize: 19,
                            color: Color(0xffffffff),
                            fontWeight: FontWeight.w700,
                          ),
                          textAlign: TextAlign.left,
                          ),
                          style: ButtonStyle(
                            backgroundColor: MaterialStateProperty.all<Color>(corBotao),
                            padding: MaterialStateProperty.all<EdgeInsetsGeometry>(const EdgeInsets.fromLTRB(20, 20, 20, 20)),
                            shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                              RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(50),
                              ),
                            ),
                            iconColor: MaterialStateProperty.all<Color>(const Color(0xFFFFFFFF)),
                            minimumSize: MaterialStateProperty.all<Size>(Size(MediaQuery.of(context).size.width * 0.7, 0))
                          )),
                      SizedBox(height: MediaQuery.of(context).size.height * 0.03),
                      ElevatedButton.icon(
                        onPressed: () {}, 
                        icon: const Icon(Icons.email), 
                        label: const Text(
                          "Login with Microsoft",
                            style: TextStyle(
                            fontFamily: 'Roboto',
                            fontSize: 19,
                            color: Color(0xffffffff),
                            fontWeight: FontWeight.w700,
                          ),
                          textAlign: TextAlign.left,
                          ),
                          style: ButtonStyle(
                            backgroundColor: MaterialStateProperty.all<Color>(corBotao),
                            padding: MaterialStateProperty.all<EdgeInsetsGeometry>(const EdgeInsets.fromLTRB(20, 20, 20, 20)),
                            shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                              RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(50),
                              ),
                            ),
                            iconColor: MaterialStateProperty.all<Color>(const Color(0xFFFFFFFF)),
                            minimumSize: MaterialStateProperty.all<Size>(Size(MediaQuery.of(context).size.width * 0.7, 0))
                          )),
                      const Spacer(),
                      Text(appVersion.join('.'), style: const TextStyle(fontSize: 10)),
                    ]),
              ),
            )));
  }
}