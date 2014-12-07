angular.module('starter.controllers', ['ngCookies'])

.controller('IntroCtrl', function($scope,$rootScope,$http,$cookies) {
        $rootScope.in = false;
         $scope.nextPage = '#/tab/dash';
         var user = $cookies.puppyEarth;    
         
         if( user === undefined) {
             $scope.nextPage = '#/register';
         } else {
            $http.get($rootScope.host+"/ping/" + user)
            .success(function (data) {
                $scope.nextPage = '#/tab/home';
            }).error(function () {
                $scope.nextPage = '#/register';
            });
             
         }
         
        

})

.controller('RegisterCtrl', function($scope,$rootScope, $http,$timeout,$location,$cookies,$ionicLoading) {
    $scope.countries = []
    $timeout(function() {
        $http.get($rootScope.host+"/countries")
            .success(function (data) {
                $scope.countries = data
            })
        
    },100)
    $scope.register = function(country) {
        $ionicLoading.show({ template: 'Please Wait' });
        $http.post( $rootScope.host + "/register", 
                    { country: country }
        ).success(function (data) {
            $ionicLoading.hide();
            $cookies.puppyEarth = data.cookie
            $location.path ("/tab/home")
        })
        
    }
    
})
.controller('HomeCtrl', function($scope,$rootScope,$location) {
})

.controller('StatsCtrl', function($scope,$rootScope, $http) {

})
.controller('SelectCtrl', function($scope,$rootScope, $http,$cookies,$location) {
    $scope.food = [ {"image": "yoghurt-granola-fruit.png", "id": 94, "name": "Yogurt, Seasonal Fruit, Granola"} ]
    
    $scope.select = function(id) {
        $location.path( "/tab/good" )
        //$http.post( $rootScope.host + "/food_choice", 
        //    { registration:  $cookies.puppyEarth , food_id: id }
        //).success(function (data) {
        //    console.log(data)
        //    $location.path = "/good"
        //})

        
    }
})

.controller('ResultCtrl', function($scope,$rootScope, $http) {

})


.controller('TasksCtrl', function($scope) {
    
});
