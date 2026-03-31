import 'package:flutter/foundation.dart';

class AppConfig {
  static String get apiBaseUrl {
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

  static String get wsBaseUrl {
    final base = apiBaseUrl.replaceFirst('http://', 'ws://').replaceFirst('https://', 'wss://');
    return base;
  }
}
