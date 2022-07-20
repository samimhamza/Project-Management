from xmlrpc.client import Server
from rest_framework.response import Response
from clients.models import Feature, PricePlan, ClientFeature, Service, ClientService
from rest_framework import status


def clientFeaturesFormatter(clientData):
    products = []
    for clientfeature in clientData['features']:
        feature = clientfeature['feature'] if clientfeature['feature'] else {}
        if clientfeature['feature']:
            del clientfeature['feature']
        feature.update(clientfeature)
        product = feature['product'] if feature['product'] else {}
        if feature['product']:
            del feature['product']
        product["features"] = []
        product["features"].append(feature)
        products.append(product)

    del clientData['features']
    clientData['products'] = []
    clientData['products'] = products
    return clientData


def clientServicesFormatter(clientData):
    services = []
    for service in clientData['services']:
        service_obj = service['service']
        del service['service']
        client_service = service
        service_obj.update(client_service)
        services.append(service_obj)
    clientData['services'] = services
    return clientData


def setProducts(new_client, data):
    if "products" in data:
        for product in data['products']:
            for feature in product['features']:
                try:
                    feature_obj = Feature.objects.get(pk=feature['feature_id'])
                except Feature.DoesNotExist:
                    return Response({"error": "Feature does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    price = PricePlan.objects.get(pk=feature['price_plan'])
                except PricePlan.DoesNotExist:
                    return Response({"error": "PricePlan does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                ClientFeature.objects.create(
                    feature=feature_obj,
                    plan=price.plan_name,
                    on_request_price=price.plan_price,
                    client=new_client
                )


def setServices(new_client, data):
    if "services" in data:
        for service in data['services']:
            try:
                service_obj = Service.objects.get(pk=service["service_id"])
            except Service.DoesNotExist:
                return Response({"error": "Feature does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            ClientService.objects.create(
                client=new_client, service=service_obj, details=service['details'] if "details" in service['details'] else "")
