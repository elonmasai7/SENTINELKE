import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'screens/ai_alerts_screen.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'screens/operations_live_screen.dart';
import 'screens/workspace_screen.dart';
import 'screens/ai_assistant_screen.dart';
import 'screens/desktop_shell_screen.dart';

void main() {
  runApp(const SentinelKEFieldKit());
}

class SentinelKEFieldKit extends StatelessWidget {
  const SentinelKEFieldKit({super.key});

  static bool _isDesktop() {
    if (kIsWeb) return false;
    return defaultTargetPlatform == TargetPlatform.windows ||
        defaultTargetPlatform == TargetPlatform.macOS ||
        defaultTargetPlatform == TargetPlatform.linux;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SentinelKE Field Kit',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorSchemeSeed: const Color(0xFF0B3D5C), useMaterial3: true),
      routes: {
        '/': (context) => const LoginScreen(),
        '/home': (context) => _isDesktop() ? const DesktopShellScreen() : const HomeScreen(),
        '/ops-live': (context) => const OperationsLiveScreen(),
        '/ai-alerts': (context) => const AiAlertsScreen(),
        '/workspace': (context) => const WorkspaceScreen(),
        '/ai-assistant': (context) => const AIAssistantScreen(),
      },
    );
  }
}
