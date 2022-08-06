from clients.models import Feature, PricePlan, ClientFeature, Service, ClientService
from rest_framework.response import Response
from rest_framework import status
from tasks.models import Task
import datetime
import pytz
import businesstimedelta



def clientProductsFormatter(clientData):
    products = []
    for clientfeature in clientData['features']:
        feature = clientfeature['feature'] if clientfeature['feature'] else {}
        del clientfeature['feature']
        feature.update(clientfeature)
        if "product" in feature:
            product = feature['product']
            del feature['product']
            hasProduct = False
            for x in products:
                if x["id"] == product["id"]:
                    hasProduct = True
                    x["features"].append(feature)
                    break
            if hasProduct == False:
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


def projectTiming(projects):
    result = []
    for project in projects:
        pro_obj = {}
        pro_obj['name'] = project['name']
        pro_obj['overdue'] = 0
        pro_obj['normal'] = 0
        pro_obj['earlier'] = 0
        pro_obj['notclear'] = 0
        pro_obj['total_tasks'] = len(project['tasks']);

        for task in project['tasks']:
            if task['p_start_date'] is None or task['p_end_date'] is None or task['a_start_date'] is None or task['a_end_date'] is None :
                pro_obj['notclear'] = pro_obj['notclear'] + 1;
            else:
                workday = businesstimedelta.WorkDayRule(
                    start_time=datetime.time(8),
                    end_time=datetime.time(17),
                    working_days=[0, 1, 2, 3, 4,5])
                lunchbreak = businesstimedelta.LunchTimeRule(
                    start_time=datetime.time(12),
                    end_time=datetime.time(13),
                    working_days=[0, 1, 2, 3, 4, 5])

                businesshrs = businesstimedelta.Rules([workday, lunchbreak])
                taskModel = Task.objects.get(id=task['id'])
                planDiff = businesshrs.difference(taskModel.p_start_date , taskModel.p_end_date)
                actualDiff = businesshrs.difference(taskModel.a_start_date , taskModel.a_end_date)

                if planDiff.hours < actualDiff.hours:
                    pro_obj['overdue'] = pro_obj['overdue'] + 1;
                elif planDiff.hours > actualDiff.hours:
                    pro_obj['earlier'] = pro_obj['earlier'] + 1;
                elif planDiff.hours == actualDiff.hours:
                    pro_obj['normal'] = pro_obj['normal'] + 1;

        result.append(pro_obj)
    return result


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
