from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime, timedelta
from myapps import pymongodb
from dashboard.models import CameraLog, Camera, Customer, Product
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

# Create your views here.
def index(request):
    template = loader.get_template('index.html')

    context = {
        'cameras' : Camera.objects.all(),
        'customers' : Customer.objects.all(),
        'products' : Product.objects.all(),
        'no' : 0,
    }
    return HttpResponse(template.render(context, request))

def camera(request, no):
    template = loader.get_template('camera.html')
    context = {
        'cameras' : Camera.objects.all(),
        'customers' : Customer.objects.all(),
        'products' : Product.objects.all(),
        'no' : no,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def searchCameraLog(request, camera_no):
    now = timezone.localtime()
    earlier = now - timedelta(seconds=1)
    context = []
    cameralogs = CameraLog.objects.filter(datetime_now__gte=earlier)
    
    for cameralog in cameralogs:
        camera_log = {}
        
        camera_log['camera_no'] = cameralog.camera.camera_no
        if(cameralog.camera.product):
            camera_log['product_no'] = cameralog.camera.product.product_no
        if(cameralog.customer):
            customer = cameralog.customer
            camera_log['customer_no'] = customer.customer_no
            camera_log['customer_name'] = customer.customer_name
            camera_log['customer_gender'] = customer.customer_gender
            camera_log['customer_age'] = customer.customer_age
            camera_log['customer_market_in'] = customer.customer_market_in
            

        for k, v in customer.customer_ratings.__dict__.items():
            if k == '_state': continue
            camera_log[str(k)] = int(v)
    
        camera_log['datetime_now'] = str(cameralog.datetime_now)
    # #print(customer.customer_no)
        context.append(camera_log)

    #     context = {'camera_log' : camera_log,'customer_log' : customer_log, 'customer_ratings' : customer_ratings}
    return HttpResponse(json.dumps(context), "application/json")