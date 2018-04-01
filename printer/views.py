import json
from django.http import JsonResponse
from printer.models import Printer, Contact
from printer.serializers import PrinterSerializer, ContactSerializer
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def printers_api(request):
    if request.method == "GET":
        printers = [printer for printer in Printer.objects.values()]  # not appropriate for real world usages
        response = []
        for printer in printers:
            serializer = PrinterSerializer(data=printer)
            response.append(serializer.data)
        return JsonResponse(response, safe=False)

    elif request.method == "POST":
        body = json.loads(request.body)
        serializer = PrinterSerializer(data=body)
        return JsonResponse(serializer.save())


@require_http_methods(["GET", "POST"])
def contact_api(request):
    if request.method == "GET":
        contacts = [contact for contact in Contact.objects.values()]  # not appropriate for real world usages
        response = []
        for contact in contacts:
            serializer = ContactSerializer(data=contact)
            response.append(serializer.data)
        return JsonResponse(response, safe=False)

    elif request.method == "POST":
        body = json.loads(request.body)
        serializer = ContactSerializer(data=body)
        return JsonResponse(serializer.save())


