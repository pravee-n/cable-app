angular.module('cableApp', [function() {

}])

.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
})

/*.controller('headerCtrl', ['$scope', '$http', function($scope, $http) {
	$scope.customer = {
		'name': '',
		'address': '',
		'phone': '',
		'subscription_date': '',
		'monthly_charge': '',
	};

	$('.js-new-date').datepicker({
		format: 'dd-mm-yyyy',
		autoclose: true
	});

	$scope.submitNewCustomer = function() {
		var url = '/addNewCustomer/';
		// var subscriptionDate = $('.js-new-date').val().split('-').reverse().join('-')
		var subscriptionDate = $('.js-new-date').val();
		$scope.customer.subscription_date = subscriptionDate;
		console.log($scope.customer);

		// return;
		$http.post(url, $scope.customer)
			.success(function(res) {
				if (res.sc == '700') {
					alert('Added successfully.');
					window.location = '/';
				}
				else {
					alert('Error !!');
				}
			})
			.error(function() {

			});

	};
}])*/

.controller('indexCtrl', ['$scope', '$http', function($scope, $http) {
	console.log('indexCtrl');
	$scope.customer = {
		'name': '',
		'address': '',
		'phone': '',
		'subscription_date': '',
		'monthly_charge': '',
		'type': 'den'
	};

	$scope.search = {
		type: 'vcno',
		query: ''
	};

	$('.js-new-date').datepicker({
		format: 'dd-mm-yyyy',
		autoclose: true
	});

	$('.js-pending-date').datepicker({
		format: "mm-yyyy",
	    startView: "months",
	    minViewMode: "months",
		autoclose: true
	});

	$scope.submitNewCustomer = function() {
		var url = '/addNewCustomer/';
		// var subscriptionDate = $('.js-new-date').val().split('-').reverse().join('-')
		var subscriptionDate = $('.js-new-date').val();
		$scope.customer.subscription_date = subscriptionDate;
		console.log($scope.customer);

		$http.post(url, $scope.customer)
			.success(function(res) {
				if (res.sc == '700') {
					alert('Added successfully.');
					window.location = '/customer/' + res.id;
				}
				else if (res.sc == '601') {
					alert(res.message);
				}
				else {
					alert('Error !!');
				}
			})
			.error(function() {

			});
	};

	$scope.viewPending = function() {
		var pendingMonthYear = $('.js-pending-date').val();
		window.location = '/pending?m=' + pendingMonthYear.split('-')[0] + '&y=' + pendingMonthYear.split('-')[1];
	};

	$scope.doSearch = function() {
		window.location = '/search?ty=' + $scope.search.type + '&q=' + $scope.search.query;
	};
}])

.controller('homeCtrl', ['$scope', '$location', function($scope, $location) {
	var customerText = $.trim($('.js-hm-data').text()),
		customerData = angular.fromJson(customerText),
		i = 0;

	$scope.customers = [];
	console.log($location);
	console.log($location.search().ty);

	for (i = 0; i < customerData.length; i++) {
		$scope.customers.push(customerData[i]);
	}
	console.log($scope.customers);

	$('.js-type').change(function() {
		console.log($(this).val());
		if ($(this).val() == 0) {
			window.location = '/customers';
		}
		else {
			window.location = '/customers?ty=' + $(this).val();
		}


	});
}])

.controller('customerCtrl', ['$scope', '$http', function($scope, $http) {
	var customerText = $.trim($('.js-cust-data').text()),
		customerData = angular.fromJson(customerText);

	$scope.selectedMonths = [];

	// customerData.subscription_date = customerData.subscription_date.split('-').reverse().join('-');
	// customerData.payment_history = angular.fromJson(customerData.payment_history);
	$scope.customer = customerData;
	console.log(customerData);
	if ($scope.customer.payment_history === '') {
		$scope.paymentHistory = {};
	}
	else {
		$scope.paymentHistory = angular.fromJson($scope.customer.payment_history);
	}

	// console.log($scope.customer);
	console.log($scope.paymentHistory);

	$('.js-update-date').datepicker({
		format: 'dd-mm-yyyy',
		autoclose: true
	});

	$('.js-pay-date').datepicker({
		format: 'dd-mm-yyyy',
		autoclose: true,
	});

	$('.js-bulk-pay-date').datepicker({
		format: 'dd-mm-yyyy',
		autoclose: true,
	});

	/*$scope.payment = {
		'date': '',
		'amount': ''
	};*/

	$scope.bulkPayment = {};

	$scope.updateCustomer = function() {
		var url = '/updateCustomer/' + $scope.customer.c_id + '/';
		// var subscriptionDate = $('.js-update-date').val().split('-').reverse().join('-')
		var subscriptionDate = $('.js-update-date').val();
		$scope.customer.subscription_date = subscriptionDate;
		// console.log($scope.customer);

		// return;
		$http.post(url, $scope.customer)
			.success(function(res) {
				if (res.sc == '700') {
					alert('Updated successfully.');
					location.reload();
				}
				else if (res.sc == '601') {
					alert(res.message);
				}
				else {
					alert('Error !!');
				}
			})
			.error(function() {

			});
	};

	$scope.delCustomer = function() {
		var deleteConfirm = confirm("Are you sure you want to delete?");
		if (deleteConfirm) {
			var url = '/deleteCustomer/' + $scope.customer.c_id + '/';

			$http.post(url)
				.success(function(res) {
					if (res.sc == '700') {
						alert('Deleted successfully.');
						window.location = '/';
					}
					else {
						alert('Error !!');
					}
				})
				.error(function() {

				});
		}
	};

	/*$scope.addPayment = function() {
		var url = '/addPayment/' + $scope.customer.c_id + '/';
		// var paymentDate = $('.js-pay-date').val().split('-').reverse().join('-');
		var paymentDate = $('.js-pay-date').val();
		$scope.payment.date = paymentDate;
		$scope.payment.year = paymentDate.split('-')[2];
		$scope.payment.month = paymentDate.split('-')[1];

		console.log($scope.payment);

		// return;
		$http.post(url, $scope.payment)
			.success(function(res) {
				if (res.sc == '700') {
					alert('Payment Added successfully.');
					location.reload();
				}
				else {
					alert('Error !!');
				}
			})
			.error(function() {

			});
	};*/

	$scope.addBulkPayment = function() {
		var url = '/addBulkPayment/' + $scope.customer.c_id + '/';
		var paymentDate = $('.js-bulk-pay-date').val();
		$scope.bulkPayment.date = paymentDate;
		$scope.bulkPayment.year = paymentDate.split('-')[2];
		$scope.bulkPayment.months = $scope.selectedMonths;

		console.log($scope.bulkPayment);

		// return;
		$http.post(url, $scope.bulkPayment)
			.success(function(res) {
				if (res.sc == '700') {
					alert('Payment Added successfully.');
					location.reload();
				}
				else {
					alert('Error !!');
				}
			})
			.error(function() {

			});
	};

	$scope.toggleSelectedMonth = function toggleSelection(value) {
	    var idx = $scope.selectedMonths.indexOf(value);

	    // is currently selected
	    if (idx > -1) {
	      $scope.selectedMonths.splice(idx, 1);
	    }

	    // is newly selected
	    else {
	      $scope.selectedMonths.push(value);
	    }
	  };


}]);