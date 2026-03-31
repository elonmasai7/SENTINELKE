from django.urls import path
from .views import africastalking_ussd, forensic_ingest

urlpatterns = [
    path('forensics/ingest/', forensic_ingest, name='forensic-ingest'),
    path('ussd/africastalking/', africastalking_ussd, name='africastalking-ussd'),
]
