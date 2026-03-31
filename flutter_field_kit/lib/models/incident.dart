class Incident {
  final String title;
  final String details;
  final double latitude;
  final double longitude;

  Incident({required this.title, required this.details, required this.latitude, required this.longitude});

  Map<String, dynamic> toJson() => {
        'title': title,
        'details': details,
        'latitude': latitude,
        'longitude': longitude,
      };
}
