var myApp = angular.module("myApp", ["ui.router"]);

myApp.config(function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/missing");

  $stateProvider.state({
    name: "missing",
    url: "/missing",
    templateUrl: "/html/missing",
    controller: "MissingController",
  });

  $stateProvider.state({
    name: "missing.who",
    url: "/who/:who",
    templateUrl: "/html/missing",
    controller: "MissingController",
  });

  $stateProvider.state({
    name: "missingreports",
    url: "/missingreports",
    templateUrl: "/html/missingreports",
    controller: "MissingReportsController",
  });

  $stateProvider.state({
    name: "associates",
    url: "/associates",
    templateUrl: "/html/associates",
    controller: "AssociatesController",
  });
  
  $stateProvider.state({
    name: "associates.hire",
    url: "/hire",
    templateUrl: "/html/associates",
    controller: "AssociatesController",
  });

  $stateProvider.state({
    name: "associate",
    url: "/associate/:id",
    templateUrl: "/html/associate",
    controller: "AssociateReportingController",
  });

  $stateProvider.state({
    name: "amenities",
    url: "/amenities",
    templateUrl: "/html/amenities",
    controller: "AmenitiesController",
  });

  $stateProvider.state({
    name: "configs",
    url: "/configs",
    templateUrl: "/html/configs",
    controller: "ConfigsController",
  });
});


myApp.service("APIService", ["$http", function($http) {
	var api = "/api";
	return {
		"missing_save": function(data){
			return $http({
				method: "POST",
				url: api+"/missing/save",
				data: data
			});
		},
		"missing_remove": function(data){
			//alert(data.id);
			return $http({
				method: "POST",
				url: api+"/missing/remove",
				data: data
			});
		},
		"missing_list": function(data){
			return $http({
				method: "POST",
				url: api+"/missing/list",
				data: data
			});
		},
        "missing_reports": function(data){
			return $http({
				method: "POST",
				url: api+"/missing/reports",
				data: data
			});
		},
		"associates_list": function(data){
			return $http({
				method: "POST",
				url: api+"/associates/list",
				data: data
			});
		},
		"associate_details": function(data){
			return $http({
				method: "POST",
				url: api+"/associate/details",
				data: data
			});
		},
		"associates_entries": function(data){
			return $http({
				method: "POST",
				url: api+"/associates/entries",
				data: data
			});
		},
		"missing_reports_individual": function(data){
			return $http({
				method: "POST",
				url: api+"/missing/reports/individual",
				data: data
			});
		},
		"amenities_list": function(data){
			return $http({
				method: "POST",
				url: api+"/amenities/list",
				data: data
			});
		},
		"amenities_remove": function(data){
			return $http({
				method: "POST",
				url: api+"/amenities/remove",
				data: data
			});
		},
		"amenities_save": function(data){
			return $http({
				method: "POST",
				url: api+"/amenities/save",
				data: data
			});
		},
		"configs_list": function(data){
			return $http({
				method: "POST",
				url: api+"/configs/list",
				data: data
			});
		},
	};
}]);


myApp.controller("MissingController", ["$scope", "$state", "$stateParams", "APIService", function($scope, $state, $stateParams, APIService) {
	$scope.today = new Date();

	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth() + 1; //January is 0!
	var yyyy = today.getFullYear();
	if (dd < 10) {
	  dd = "0" + dd;
	} 
	if (mm < 10) {
	  mm = "0" + mm;
	}
	var dateControl = document.querySelector('input[type="date"]');
	dateControl.max = yyyy + "-" + mm + "-" + dd;
	//dateControl.min = "2019-08-01"; // yyyy + "-" + mm + "-" + dd;
	
	
	$scope.amenities = [];
	$scope.amenities_list = function()
    {
		APIService.amenities_list()
		.then(function(response){
			$scope.amenities = response.data;
	    }, function(error){
			alert("Error loading amenities data...");
	    });
    };
	$scope.amenities_list();

	var who = $stateParams.who?$stateParams.who:""; // from different routing: /who
	$scope.missing = {};
	$scope.missingdefaults = function(){
		$scope.missing = {
			"date": new Date(),
			"associate": who,
			"room_number": "",
			"missingstuffs": "",
			"anc": "",
			"remarks": "",
		};
	};
	$scope.missingdefaults();

    $scope.save = function(missing)
    {
		// validations
		if(missing.date=="" || missing.date==null) return false;
		if(missing.associate=="") return false;
		//if(missing.room_number=="-") return false;
		if(missing.missingstuffs=="" && missing.anc=="" && missing.remarks=="") return false;

		APIService.missing_save(missing)
		.then(function(response){
			$scope.missingdefaults();
			$scope.list();
	    }, function(error){
			alert("Error saving data...");
	    });
    };

    $scope.remove = function(missing_id)
    {
		if(window.confirm("Remove record?"))
		{
			APIService.missing_remove({"id": missing_id})
			.then(function(response){
				$scope.missingdefaults();
				$scope.list();
			}, function(error){
				alert("Error removing data.."+error.data);
			});
		}
    };

	$scope.missingdata = [];
	$scope.list = function()
    {
		APIService.missing_list()
		.then(function(response){
			$scope.missingdata = response.data;
	    }, function(error){
			alert("Error loading missing data...");
	    });
    };
	$scope.list();

	$scope.associates = [];
	$scope.associates_list = function()
    {
		APIService.associates_list()
		.then(function(response){
			$scope.associates = response.data;
	    }, function(error){
			alert("Error loading associates data...");
	    });
    };
	$scope.associates_list();

}]);


myApp.controller("MissingReportsController", ["$scope", "$state", "$stateParams", "APIService", function($scope, $state, $stateParams, APIService) {
    $scope.missingdata = [];
	$scope.list = function()
    {
		APIService.missing_reports()
		.then(function(response){
			$scope.missingdata = response.data;
	    }, function(error){
			alert("Error loading missing data...");
	    });
    };
	$scope.list();
}]);


myApp.controller("AssociatesController", ["$scope", "$state", "$stateParams", "APIService", function($scope, $state, $stateParams, APIService) {
    $scope.associates = [];
	$scope.associates_list = function()
    {
		APIService.associates_list()
		.then(function(response){
			$scope.associates = response.data;
			
			var promises=[];
			angular.forEach(response.data, function(value, key) {
				APIService.associates_entries({"id": value[0]})
				.then(function(response_individual){
					value.push(response_individual.data[2]);
				}, function(error){
				});
			}, promises);



	    }, function(error){
			alert("Error loading associates data...");
	    });
    };
	$scope.associates_list();
	
	$scope.fire = function(who)
	{
		alert("Please ask your admin.");
	};
}]);


myApp.controller("AssociateReportingController", ["$scope", "$state", "$stateParams", "APIService", function($scope, $state, $stateParams, APIService) {
    $scope.missingdata = [];
	$scope.list = function()
    {
		APIService.missing_reports_individual({"id": $stateParams.id})
		.then(function(response){
			$scope.missingdata = response.data;
	    }, function(error){
			alert("Error loading missing data...");
	    });
    };
	$scope.list();
	
	$scope.associate = {};
	$scope.associate_details = function()
    {
		APIService.associate_details({"id": $stateParams.id})
		.then(function(response){
			$scope.associate = response.data;
	    }, function(error){
			alert("Error loading associate data...");
	    });
    };
	$scope.associate_details();
}]);


myApp.controller("AmenitiesController", ["$scope", "$state", "$stateParams", "APIService", function($scope, $state, $stateParams, APIService) {
    $scope.amenities = [];
	$scope.amenities_list = function()
    {
		APIService.amenities_list()
		.then(function(response){
			$scope.amenities = response.data;
	    }, function(error){
			alert("Error loading amenities data...");
	    });
	    
	    document.getElementById("amenity-name").focus();
    };
	$scope.amenities_list();

	$scope.amenity = {"name": ""};
	$scope.save = function(amenity)
    {
		if(amenity.name=="") return false;
		if(amenity.name=="-") return false;

		APIService.amenities_save(amenity)
		.then(function(response){
			$scope.amenity = {"name": ""};
			$scope.amenities_list();
	    }, function(error){
			alert("Error saving amenity data...");
	    });
    };
	
	$scope.remove = function(amenity)
    {
		if(window.confirm("Remove record?"))
		{
			APIService.amenities_remove({"id": amenity[0]})
			.then(function(response){
				$scope.amenities_list();
			}, function(error){
				alert("Error removing amenity...");
			});
		}
    };
}]);


myApp.controller("ConfigsController", ["$scope", "$state", "$stateParams", "APIService", function($scope, $state, $stateParams, APIService) {
    $scope.configs = [];
	$scope.configs_list = function()
    {
		APIService.configs_list()
		.then(function(response){
			$scope.configs = response.data;
	    }, function(error){
			alert("Error loading configs data...");
	    });
    };
	$scope.configs_list();
}]);
