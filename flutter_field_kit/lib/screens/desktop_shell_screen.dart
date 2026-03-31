import 'package:flutter/material.dart';

import 'ai_alerts_screen.dart';
import 'ai_assistant_screen.dart';
import 'operations_live_screen.dart';
import 'workspace_screen.dart';

class DesktopShellScreen extends StatefulWidget {
  const DesktopShellScreen({super.key});

  @override
  State<DesktopShellScreen> createState() => _DesktopShellScreenState();
}

class _DesktopShellScreenState extends State<DesktopShellScreen> {
  int _selectedIndex = 0;

  static const _titles = [
    'Live Command Dashboard',
    'AI Threat Alerts',
    'Joint Workspace',
    'AI Assistant',
  ];

  final List<Widget> _pages = const [
    OperationsLiveScreen(),
    AiAlertsScreen(),
    WorkspaceScreen(),
    AIAssistantScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: _selectedIndex,
            onDestinationSelected: (index) => setState(() => _selectedIndex = index),
            extended: true,
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.map),
                label: Text('Operations'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.warning_amber),
                label: Text('AI Alerts'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.groups),
                label: Text('Workspace'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.smart_toy),
                label: Text('AI Assistant'),
              ),
            ],
          ),
          const VerticalDivider(width: 1),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                  child: Text(
                    _titles[_selectedIndex],
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                ),
                const Divider(height: 1),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: _pages[_selectedIndex],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
