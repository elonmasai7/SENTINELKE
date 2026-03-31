import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const SentinelKEFieldKit());
}

class SentinelKEFieldKit extends StatelessWidget {
  const SentinelKEFieldKit({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SentinelKE Field Kit',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorSchemeSeed: const Color(0xFF0B3D5C), useMaterial3: true),
      routes: {
        '/': (context) => const LoginScreen(),
        '/home': (context) => const HomeScreen(),
      },
    );
  }
}
