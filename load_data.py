import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "printer_home_work.settings")
import django
django.setup()
from printer.models import Printer, Contact

Printer.objects.create(
    name='test',
    min_production_time=1,
    max_production_time=10
)
Contact.objects.create(
    first_name='matan',
    last_name='shalit',
    id_number='123456',
    city='ramat gan',
    street='haroe',
    house_number=93,
    apartment_floor=1,
    house_entrance='a',
    apartment_number=7
)
