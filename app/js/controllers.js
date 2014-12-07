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
.controller('HomeCtrl', function($scope,$rootScope,$http,$location,$cookies) {
    $scope.total_tasks = 0;
    $scope.total_points = 0;
    
     $http.get($rootScope.host+"/user?registration=" + $cookies.puppyEarth)
            .success(function (data) {
                $scope.total_tasks = data.total_tasks;
                $scope.total_points = data.total_points;
                
                $('#points').sparkline([10,6,7,8,9,10],
                    {
                        type: 'bar',
                        height: '40',
                        barWidth: 6,
                        chartRangeMin :0,
                        chartRangeMax :10,
                        barColor: '#00bf00',
                        negBarColor: '#f04040 '
                    });
                $('#tasks').easyPieChart({
                    barColor: '#00bf00',
                    trackColor: '#E2E2E2',
                    scaleColor: false,
                    lineCap: 'butt',
                    lineWidth: 5,
                    animate: 1000,
                    size: 50
                });        
                
            })
})

.controller('StatsCtrl', function($scope,$rootScope, $http) {

})
.controller('SelectCtrl', function($scope,$rootScope, $http,$cookies,$location,$timeout) {
    $scope.food = []
    $timeout(function() {
        $http.get($rootScope.host+"/foods")
            .success(function (data) {
                $scope.food = data
            })
        
    },100)
    
    
    $scope.select = function(id) {
       
        $http.post( $rootScope.host + "/food_choice", 
            { registration:  $cookies.puppyEarth , food_id: id }
        ).success(function (data) {
            console.log(data)
             if( data.score <= 0 ) {
                $location.path( "/tab/good/" + Math.abs(data.score) )
             } else {
                $location.path( "/tab/bad/" + Math.abs(data.score) )
             }
        })

        
    }
})

.controller('ResultCtrl', function($scope,$stateParams, $http) {
    $scope.good = "healthy.png"
    $scope.bad = "bad" + (Math.floor(Math.random() * 3) + 1) + ".png"
    $scope.score = $stateParams.score

})


.controller('TasksCtrl', function($scope) {
    
});
