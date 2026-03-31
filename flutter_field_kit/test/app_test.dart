import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sentinelke_field_kit/main.dart';

void main() {
  testWidgets('login screen renders and navigates to home', (WidgetTester tester) async {
    await tester.pumpWidget(const SentinelKEFieldKit());

    expect(find.text('SentinelKE Field Kit'), findsOneWidget);
    expect(find.text('Authenticate'), findsOneWidget);

    await tester.tap(find.text('Authenticate'));
    await tester.pumpAndSettle();

    expect(find.text('Field Operations'), findsOneWidget);
  });
}
