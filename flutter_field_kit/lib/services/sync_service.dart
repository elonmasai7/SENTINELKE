import 'dart:convert';
import 'package:http/http.dart' as http;

class SyncService {
  final String apiBaseUrl;

  SyncService({required this.apiBaseUrl});

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
}
