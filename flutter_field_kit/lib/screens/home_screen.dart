import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Field Operations')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: ListTile(
              title: const Text('Live Command Dashboard'),
              subtitle: const Text('Asset and incident stream with threat overlays'),
              onTap: () => Navigator.pushNamed(context, '/ops-live'),
            ),
          ),
          Card(
            child: ListTile(
              title: const Text('AI Threat Alerts'),
              subtitle: const Text('Pattern-of-life and predictive threat notifications'),
              onTap: () => Navigator.pushNamed(context, '/ai-alerts'),
            ),
          ),
          Card(
            child: ListTile(
              title: const Text('Joint Workspace'),
              subtitle: const Text('Case notes and inter-agency collaboration channel'),
              onTap: () => Navigator.pushNamed(context, '/workspace'),
            ),
          ),
          Card(
            child: ListTile(
              title: const Text('AI Assistant Gateway'),
              subtitle: const Text('Secure query, case brief, and field intelligence assistant'),
              onTap: () => Navigator.pushNamed(context, '/ai-assistant'),
            ),
          ),
          const Card(
            child: ListTile(
              title: Text('Offline Integrity Queue'),
              subtitle: Text('Cryptographically signed offline logs pending sync'),
            ),
          ),
        ],
      ),
    );
  }
}
