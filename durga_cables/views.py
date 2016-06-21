from django.http import HttpResponse
from django.shortcuts import render, redirect
import pdb
from django.views.decorators.csrf import csrf_exempt
import json
from durga_cables.models import *


def home(request):
	customers = Customer.objects.all();
	customer_data = []
	for customer in customers:
		customer_data.append({
			'name': customer.name,
			'address': customer.address,
			'cid': customer.id
		})
	ctx = {
		'customer_data': json.dumps(customer_data)
	}
	return render(request, 'home.html', ctx)
	# return HttpResponse("Hello World!");


@csrf_exempt
def addNewCustomer(request):
	pdb.set_trace()
	try:
		customerData = json.loads(request.body);
		# payment_data = {}
		customer = Customer(
	                name = str(customerData['name']),
	                address = str(customerData['address']),
	                subscription_date = str(customerData['subscription_date']),
	                phone = str(customerData['phone']),
	                monthly_charge = str(customerData['monthly_charge']),
	                payment_history = ''
	            ).save()

		responseJson = {
		   'sc': '700',
		}
	except Exception as inst:
		responseJson = {
		   'sc': '600',
		}

	responseJsonDump = json.dumps(responseJson)
	return HttpResponse(responseJsonDump, content_type="application/json")


def viewCustomer(request, c_id):
	customer_id = str(c_id);
	# pdb.set_trace()
	customer = Customer.objects.get(id=customer_id);
	customer_res = {
		'name': customer.name,
		'address': customer.address,
		'phone': customer.phone,
		'monthly_charge': customer.monthly_charge,
		'subscription_date': customer.subscription_date,
		'payment_history': customer.payment_history,
		'c_id': customer.id
	}
	ctx = {
		'desc': json.dumps(customer_res)
	}
	return render(request, 'customer.html', ctx)

@csrf_exempt
def updateCustomer(request, c_id):
	customer_id = str(c_id);
	customer = Customer.objects.get(id=customer_id);
	updated_data = json.loads(request.body);

	customer.name = updated_data['name']
	customer.address = updated_data['address']
	customer.phone = updated_data['phone']
	customer.monthly_charge = updated_data['monthly_charge']
	customer.subscription_date = str(updated_data['subscription_date'])
	customer.save()

	responseJson = {
	   'sc': '700',
	}

	responseJsonDump = json.dumps(responseJson)
	return HttpResponse(responseJsonDump, content_type="application/json")


@csrf_exempt
def deleteCustomer(request, c_id):
	try:
		customer_id = str(c_id);
		customer = Customer.objects.get(id=customer_id);
		customer.delete();
		responseJson = {
		   'sc': '700',
		}

	except Exception as inst:
		responseJson = {
		   'sc': '600',
		}



	responseJsonDump = json.dumps(responseJson)
	return HttpResponse(responseJsonDump, content_type="application/json")


@csrf_exempt
def addPayment(request, c_id):
	try:
		# pdb.set_trace()
		customer_id = str(c_id)
		customer = Customer.objects.get(id=customer_id)
		payment_data = json.loads(request.body)
		year = str(payment_data['year'])
		monthStr = getMonthName(str(payment_data['month']))
		month = int(payment_data['month']) - 1;

		if not customer.payment_history:
			customer.payment_history = {}
			customer.payment_history[year] = [None] * 12;
		else:
			customer.payment_history = json.loads(customer.payment_history);
		if year not in customer.payment_history:
			customer.payment_history[year] = [None] * 12;
		customer.payment_history[year][month] = {
			'month': monthStr,
			'date': str(payment_data['date']),
			'amount': int(payment_data['amount'])
		}
		customer.payment_history = json.dumps(customer.payment_history);
		customer.save()

		responseJson = {
		   'sc': '700',
		}

	except Exception as inst:
		responseJson = {
		   'sc': '600',
		}

	responseJsonDump = json.dumps(responseJson)
	return HttpResponse(responseJsonDump, content_type="application/json")

@csrf_exempt
def addBulkPayment(request, c_id):
	try:
		# pdb.set_trace()
		customer_id = str(c_id)
		customer = Customer.objects.get(id=customer_id)
		payment_data = json.loads(request.body)
		year = str(payment_data['year'])
		# monthStr = getMonthName(str(payment_data['month']))
		months = payment_data['months'];

		if not customer.payment_history:
			customer.payment_history = {}
			customer.payment_history[year] = [None] * 12;
		else:
			customer.payment_history = json.loads(customer.payment_history);

		if year not in customer.payment_history:
			customer.payment_history[year] = [None] * 12;

		for month in months:
			customer.payment_history[year][month] = {
				'month': getMonthName(month),
				'date': str(payment_data['date']),
				'amount': customer.monthly_charge
			}

		customer.payment_history = json.dumps(customer.payment_history);
		customer.save()

		responseJson = {
		   'sc': '700',
		}

	except Exception as inst:
		responseJson = {
		   'sc': '600',
		}

	responseJsonDump = json.dumps(responseJson)
	return HttpResponse(responseJsonDump, content_type="application/json")

def getMonthName(monthNum):
	if monthNum == '01' or monthNum == 0:
		return 'Jan'
	elif monthNum == '02' or monthNum == 1:
		return 'Feb'
	elif monthNum == '03' or monthNum == 2:
		return 'Mar'
	elif monthNum == '04' or monthNum == 3:
		return 'Apr'
	elif monthNum == '05' or monthNum == 4:
		return 'May'
	elif monthNum == '06' or monthNum == 5:
		return 'Jun'
	elif monthNum == '07' or monthNum == 6:
		return 'Jul'
	elif monthNum == '08' or monthNum == 7:
		return 'Aug'
	elif monthNum == '09' or monthNum == 8:
		return 'Sep'
	elif monthNum == '10' or monthNum == 9:
		return 'Oct'
	elif monthNum == '11' or monthNum == 10:
		return 'Nov'
	elif monthNum == '12' or monthNum == 11:
		return 'Dec'






