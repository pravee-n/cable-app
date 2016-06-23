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
	return render(request, 'index.html', ctx)
	# return HttpResponse("Hello World!");

def listCustomers(request):
	# pdb.set_trace();
	querySize = 50;
	start_index = int(request.GET.get('s', 0))
	end_index = int(request.GET.get('e', querySize))
	type = request.GET.get('ty')
	if type is not None:
		customers = Customer.objects.filter(type=type)[start_index:end_index];
		totalCount = Customer.objects.filter(type=type).count();
	else:
		customers = Customer.objects.all()[start_index:end_index];
		totalCount = Customer.objects.all().count();

	customer_data = []
	for customer in customers:
		customer_data.append({
			'name': customer.name,
			'address': customer.address,
			'cid': customer.id
		})
	ctx = {
		'customer_data': json.dumps(customer_data),
		'type': type
	}

	if type is not None:
		if end_index < totalCount:
			ctx['nextUrl'] = '/customers?s=' + str(end_index) + '&e=' + str(end_index + querySize) + '&ty=' + type;

		if start_index > 0:
			ctx['prevUrl'] = '/customers?s=' + str(max(0, start_index - querySize)) + '&e=' + str(start_index) + '&ty=' + type;
	else:
		if end_index <= totalCount:
			ctx['nextUrl'] = '/customers?s=' + str(end_index) + '&e=' + str(end_index + querySize);

		if start_index > 0:
			ctx['prevUrl'] = '/customers?s=' + str(max(0, start_index - querySize)) + '&e=' + str(start_index);


	ctx['countTxt'] = 'Showing ' + str(start_index + 1)  + ' - ' + str(min(totalCount, end_index)) + ' of total ' + str(totalCount) + ' records';

	return render(request, 'home.html', ctx)

def search(request):
	type = str(request.GET.get('ty'))
	q = str(request.GET.get('q'))
	search_txt = 'Searching by '
	if type == 'vcno':
		customers = Customer.objects.filter(vc_no__icontains=q)
		search_txt += 'VC no. '
	elif type == 'name':
		customers = Customer.objects.filter(name__icontains=q)
		search_txt += 'Name '
	elif type == 'phone':
		customers = Customer.objects.filter(phone__icontains=q)
		search_txt += 'Mobile no. '

	search_txt += 'for query: ' + q
	search_data = []
	for customer in customers:
		search_data.append({
			'vc_no': customer.vc_no,
			'name': customer.name,
			'phone': customer.phone,
			'address': customer.address,
			'cid': customer.id
		})
	ctx = {
		'customer_data': json.dumps(search_data),
		'search_txt': search_txt
	}
	return render(request, 'searchResults.html', ctx)

def viewPending(request):
	pdb.set_trace();
	initialPendingMonth = int(request.GET.get('m')) - 1
	initialPendingYear = int(request.GET.get('y')) - 1
	pendingMonth = int(request.GET.get('m')) - 1
	pendingYear = int(request.GET.get('y'))
	ctx = {};
	pending_customers = []
	if pendingMonth is None or pendingYear is None:
		return render(request, 'pendingCustomers.html', ctx)

	customers = Customer.objects.all();
	for customer in customers:
		pending_payment = 0;
		pendingMonth = initialPendingMonth
		pendingYear = initialPendingYear
		subscription_month = int(customer.subscription_date.split('-')[1]) - 1
		subscription_year = int(customer.subscription_date.split('-')[2])
		if not customer.payment_history:
			payment_history = {};
		else:
			payment_history = json.loads(customer.payment_history);

		if payment_history and payment_history[pendingYear] and payment_history[pendingYear][pendingMonth]:
			continue
		else:
			while pendingYear >= subscription_year:
				while pendingMonth >= subscription_month if pendingYear == subscription_year else 0:
					if not payment_history or not payment_history[pendingYear] or not payment_history[pendingYear][pendingMonth]:
						pending_payment += customer.monthly_charge;
					pendingMonth -= 1;
				pendingMonth = 11;
				pendingYear -= 1;
			pending_customers.append({
				'name': customer.name,
				'address': customer.address,
				'cid': customer.id,
				'pending_amount': pending_payment
			})

	ctx = {
		'customer_data': json.dumps(pending_customers)
	}
	return render(request, 'pendingCustomers.html', ctx)


@csrf_exempt
def addNewCustomer(request):
	# pdb.set_trace()
	try:
		customerData = json.loads(request.body);
		# payment_data = {}
		customer = Customer(
					vc_no = str(customerData['vc_no']),
					stb_no = str(customerData['stb_no']),
	                name = str(customerData['name']),
	                address = str(customerData['address']),
	                subscription_date = str(customerData['subscription_date']),
	                phone = str(customerData['phone']),
	                monthly_charge = str(customerData['monthly_charge']),
	                type = str(customerData['type']),
	                payment_history = ''
	            ).save()

		responseJson = {
		   'sc': '700',
		}
	except Exception as inst:
		if 'vc_no' in str(inst) and 'Duplicate entry' in str(inst):
			responseJson = {
			   'sc': '601',
			   'message': "This VC no. already exists."
			}
		else:
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
		'vc_no': customer.vc_no,
		'stb_no': customer.stb_no,
		'name': customer.name,
		'address': customer.address,
		'phone': customer.phone,
		'monthly_charge': customer.monthly_charge,
		'subscription_date': customer.subscription_date,
		'payment_history': customer.payment_history,
		'type': customer.type,
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

	try:
		customer.vc_no = updated_data['vc_no']
		customer.stb_no = updated_data['stb_no']
		customer.name = updated_data['name']
		customer.address = updated_data['address']
		customer.phone = updated_data['phone']
		customer.monthly_charge = updated_data['monthly_charge']
		customer.type = updated_data['type']
		customer.subscription_date = str(updated_data['subscription_date'])
		customer.save()
		responseJson = {
		   'sc': '700',
		}
	except Exception as inst:
		if 'vc_no' in str(inst) and 'Duplicate entry' in str(inst):
			responseJson = {
			   'sc': '601',
			   'message': "This VC no. already exists."
			}
		else:
			responseJson = {
			   'sc': '600',
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
