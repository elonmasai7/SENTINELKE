import 'package:flutter/material.dart';

class AIAssistantScreen extends StatefulWidget {
  const AIAssistantScreen({super.key});

  @override
  State<AIAssistantScreen> createState() => _AIAssistantScreenState();
}

class _AIAssistantScreenState extends State<AIAssistantScreen> {
  final TextEditingController _controller = TextEditingController();
  String _mode = 'cloud';
  String _lastResponse = 'No query submitted yet.';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Assistant')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Text('Mode: '),
                DropdownButton<String>(
                  value: _mode,
                  items: const [
                    DropdownMenuItem(value: 'cloud', child: Text('Cloud Routed')),
                    DropdownMenuItem(value: 'local', child: Text('Local-Only (llama.cpp)')),
                  ],
                  onChanged: (value) {
                    if (value != null) {
                      setState(() => _mode = value);
                    }
                  },
                ),
              ],
            ),
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                labelText: 'Ask AI',
                hintText: 'Summarize incidents linked to suspect X',
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 12),
            FilledButton(
              onPressed: () {
                setState(() {
                  _lastResponse = 'Request queued. Connect this screen to /api/ai/query endpoint.';
                });
              },
              child: const Text('Submit'),
            ),
            const SizedBox(height: 16),
            const Text('Response', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(_lastResponse),
          ],
        ),
      ),
    );
  }
}
