import 'package:flutter/material.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 360),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('SentinelKE Field Kit', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              const Text('Biometric authentication required'),
              const SizedBox(height: 24),
              FilledButton(
                onPressed: () => Navigator.pushReplacementNamed(context, '/home'),
                child: const Text('Authenticate'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
