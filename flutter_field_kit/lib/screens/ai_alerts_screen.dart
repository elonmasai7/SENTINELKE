import 'package:flutter/material.dart';

class AiAlertsScreen extends StatelessWidget {
  const AiAlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Threat Alerts')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          Card(child: ListTile(title: Text('Threat Score 89'), subtitle: Text('High connectivity + repeated location anomalies'))),
          Card(child: ListTile(title: Text('Pattern Deviation'), subtitle: Text('Unusual encrypted app spike at non-baseline hours'))),
        ],
      ),
    );
  }
}
