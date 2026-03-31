import 'dart:convert';
import 'package:crypto/crypto.dart';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

class LocalStore {
  Future<Database> _open() async {
    final base = await getDatabasesPath();
    final dbPath = join(base, 'sentinelke_fieldkit.db');
    return openDatabase(
      dbPath,
      version: 1,
      onCreate: (db, version) async {
        await db.execute(
          'CREATE TABLE IF NOT EXISTS offline_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT, payload_hash TEXT, signature TEXT, queued_at TEXT)',
        );
      },
    );
  }

  String _hashPayload(String payload) {
    return sha256.convert(utf8.encode(payload)).toString();
  }

  String _signPayloadHash(String payloadHash, String deviceSecret) {
    return sha256.convert(utf8.encode('$payloadHash:$deviceSecret')).toString();
  }

  Future<void> queueEncryptedPayload(Map<String, dynamic> payload, {required String deviceSecret}) async {
    final db = await _open();
    final payloadText = jsonEncode(payload);
    final payloadHash = _hashPayload(payloadText);
    final signature = _signPayloadHash(payloadHash, deviceSecret);

    await db.insert('offline_logs', {
      'payload': payloadText,
      'payload_hash': payloadHash,
      'signature': signature,
      'queued_at': DateTime.now().toUtc().toIso8601String(),
    });
  }
}
