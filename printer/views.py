import json
from django.http import JsonResponse
from printer.models import Printer
from printer.serializers import PrinterSerializer
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def get_printers(request):
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
        serializer.save()
        return JsonResponse(body)

