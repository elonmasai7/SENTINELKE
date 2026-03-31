import 'package:flutter/material.dart';

class WorkspaceScreen extends StatelessWidget {
  const WorkspaceScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Joint Task Workspace')),
      body: const Padding(
        padding: EdgeInsets.all(16),
        child: Text('Shared case annotations, investigator comments, and secure collaboration feed.'),
      ),
    );
  }
}
