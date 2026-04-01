import 'package:flutter/foundation.dart';

class AppConfig {
  static const String _apiFromEnv = String.fromEnvironment('API_BASE_URL', defaultValue: '');
  static const String _aiFromEnv = String.fromEnvironment('AI_SERVICE_URL', defaultValue: '');
  static const String _mapFromEnv = String.fromEnvironment('MAP_SERVICE_URL', defaultValue: '');
  static const String _wsFromEnv = String.fromEnvironment('WS_BASE_URL', defaultValue: '');

  static String get apiBaseUrl {
    if (_apiFromEnv.isNotEmpty) {
      return _apiFromEnv;
    }
    if (kIsWeb) {
      return 'http://127.0.0.1:8010';
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return 'http://10.0.2.2:8010';
      case TargetPlatform.iOS:
        return 'http://127.0.0.1:8010';
      default:
        return 'http://127.0.0.1:8010';
    }
  }

  static String get aiServiceUrl {
    if (_aiFromEnv.isNotEmpty) {
      return _aiFromEnv;
    }
    return 'http://127.0.0.1:9000';
  }

  static String get mapServiceUrl {
    if (_mapFromEnv.isNotEmpty) {
      return _mapFromEnv;
    }
    return 'https://tile.openstreetmap.org';
  }

  static String get wsBaseUrl {
    if (_wsFromEnv.isNotEmpty) {
      return _wsFromEnv;
    }
    final base = apiBaseUrl.replaceFirst('http://', 'ws://').replaceFirst('https://', 'wss://');
    return base;
  }
}
