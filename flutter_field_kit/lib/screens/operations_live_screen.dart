import 'package:flutter/material.dart';

class OperationsLiveScreen extends StatelessWidget {
  const OperationsLiveScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Live Command Dashboard')),
      body: const Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('WebSocket stream active', style: TextStyle(fontWeight: FontWeight.bold)),
            SizedBox(height: 12),
            Text('Real-time asset locations and threat overlays appear here.'),
          ],
        ),
      ),
    );
  }
}
