import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart';

class SyncService {
  final String apiBaseUrl;
  final String wsBaseUrl;

  SyncService({required this.apiBaseUrl, required this.wsBaseUrl});

  Future<bool> syncIncident(Map<String, dynamic> payload, String token) async {
    final response = await http.post(
      Uri.parse('$apiBaseUrl/api/geo/incidents/'),
      headers: {
        'Authorization': 'Token $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(payload),
    );
    return response.statusCode >= 200 && response.statusCode < 300;
  }

  WebSocketChannel subscribeOperationsLive() {
    return WebSocketChannel.connect(Uri.parse('$wsBaseUrl/ws/operations/live/'));
  }
}
