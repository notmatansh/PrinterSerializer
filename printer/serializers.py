from nesting_serializer import NestingSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from printer.models import Printer, Contact


class PrinterSerializer(NestingSerializer, ModelSerializer):
    """
    the serializer object given by the practice, only change i did was to add the id field
    """
    class Meta:
        # ‘model’ and ‘fields’ are options for the ModelSerializer
        model = Printer
        fields = ['id', 'name', 'min_production_time', 'max_production_time']
        # the field id was not in the initial practice setup but in order to support updating and not just
        # getting and creating i needed a unique attribute to be passed over the API

    # The ‘nesting’ option should be used by the NestingSerializer
    nesting = {
        'productionTime': {
            'minimum': 'min_production_time',
            'maximum': 'max_production_time'
        }
    }


class ContactSerializer(NestingSerializer, ModelSerializer):
    """
    a more complex serializer with a more complex data model to test and improve the NestingSerializer implementation
    """
    class Meta:
        # ‘model’ and ‘fields’ are options for the ModelSerializer
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'id_number', 'city', 'street', 'house_number', 'apartment_number',
                  'apartment_floor', 'house_entrance']
        # the field id was not in the initial setup but in order to support updating and not just
        # getting and creating i needed a unique attribute to be passed over the API

    # The ‘nesting’ option should be used by the NestingSerializer
    nesting = {
        'full_name': {
            'first': 'first_name',
            'last': 'last_name'
        },
        'address': {
            'city': 'city',
            'street': 'street',
            'house': 'house_number',
            'building_details': {
                'apartment': 'apartment_number',
                'floor': 'apartment_floor',
                'entrance': 'house_entrance'
            }

        }
    }
