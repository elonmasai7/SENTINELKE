import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Field Operations')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          Card(child: ListTile(title: Text('Report Incident'), subtitle: Text('Capture notes, media, and GPS tag'))),
          Card(child: ListTile(title: Text('Queued Sync Items'), subtitle: Text('Offline-first encrypted upload queue'))),
          Card(child: ListTile(title: Text('Emergency Alert'), subtitle: Text('Priority dispatch channel'))),
        ],
      ),
    );
  }
}
