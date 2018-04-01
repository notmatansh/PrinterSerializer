import json
from django.http import JsonResponse
from printer.models import Printer, Contact
from printer.serializers import PrinterSerializer, ContactSerializer
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict


@require_http_methods(["GET", "POST"])
def printers_api(request):
    if request.method == "GET":
        printers = [printer for printer in Printer.objects.values()]
        response = []
        for printer in printers:
            serializer = PrinterSerializer(data=printer)
            response.append(serializer.data)
        return JsonResponse(response, safe=False)  # safe=False because our response is a list of jsons

    elif request.method == "POST":
        body = json.loads(request.body)
        serializer = PrinterSerializer(data=body)
        serializer.is_valid()
        obj = serializer.save()
        # now that we have our updated/created object i will pass a dict representation of it though our serializer
        # in order to return it in our nested structure
        obj_dict = model_to_dict(obj)
        obj_data = PrinterSerializer(data=obj_dict).data
        return JsonResponse(obj_data)


@require_http_methods(["GET", "POST"])
def contact_api(request):
    if request.method == "GET":
        contacts = [contact for contact in Contact.objects.values()]
        response = []
        for contact in contacts:
            serializer = ContactSerializer(data=contact)
            response.append(serializer.data)
        return JsonResponse(response, safe=False)  # safe=False because our response is a list of jsons

    elif request.method == "POST":
        body = json.loads(request.body)
        serializer = ContactSerializer(data=body)
        serializer.is_valid()
        obj = serializer.save()
        # now that we have our updated/created object i will pass a dict representation of it though our serializer
        # in order to return it in our nested structure
        obj_dict = model_to_dict(obj)
        obj_data = ContactSerializer(data=obj_dict).data
        return JsonResponse(obj_data)


