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
.controller('HomeCtrl', function($scope,$rootScope,$http,$location,$cookies,$timeout) {
    $scope.total_tasks = 0;
    $scope.total_points = 0;
    $scope.mood = "healthy.png"
    
  
    
     $http.get($rootScope.host+"/user?registration=" + $cookies.puppyEarth)
            .success(function (data) {
                $scope.total_tasks = data.total_tasks;
                $scope.total_points = data.total_points;
                var r = (Math.floor(Math.random() * 4) + 1)
                if(r == 1) {
                    $scope.mood = "healthy.png"
                } else if(r == 2) {
                    $scope.mood = "bad2.png"
                } else  if(r == 3) {
                    $scope.mood = "hungry.png"
                }
                $('#points').sparkline(data.recent_points,
                    {
                        type: 'bar',
                        height: '40',
                        barWidth: 6,
                        chartRangeMin :0,
                        chartRangeMax :10,
                        barColor: '#9ABC32',
                        negBarColor: '#f04040 '
                    });
                $('#tasks').easyPieChart({
                    barColor: '#9ABC32',
                    trackColor: '#E2E2E2',
                    scaleColor: false,
                    lineCap: 'butt',
                    lineWidth: 5,
                    animate: 1000,
                    size: 50
                });        
                
            })
})

.controller('StatsCtrl', function($scope,$rootScope, $http ,$cookies) {
    $scope.delta = 0    
    $scope.total_debit = 0 
    $scope.total_credit = 0
    $scope.image  = "up.png"
    $scope.target = 0
    $http.get($rootScope.host+"/stats?registration=" + $cookies.puppyEarth )
        .success(function (data) {
            $scope.target = Math.abs(data.target)
            $scope.total_debit = data.total_debit
            $scope.debit_trend = data.debit_trend            
            $scope.total_credit = data.total_credit
            $scope.credit_trend = data.credit_trend
            $scope.delta = data.total_credit - data.total_debit
            if( $scope.delta > 0 ) {
                $scope.image  = "up.png"
            } else {
                $scope.image  = "down.png"
            }
            
        })
    

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
             if( data.score >= 0 ) {
                $rootScope.pubnub.publish({
                    channel: 'codegreen_channel',
                    message: {"country":data.country ,"amount":Math.abs(data.score)} });
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

}).controller('TasksCtrl', function($scope) {
    $scope.tasks = [ { id: 1, title: "Buy organically grown food"}]
}).controller('TaskCtrl', function($scope,$stateParams, $http,$location) {
    $scope.id  = $stateParams.id
    $scope.task =  { id: 1, title: "Buy organically grown food",content:"In addition to the health benefits, the pesticides and artificial fertilizers used on non ­organic food are made using lots of fossil fuel and venting much greenhouse gas."}
    
    $scope.complete = function(id) {
        alert("complete " + id)
        $location.path("/tab/tasks")
    }
    
    $scope.dismiss = function(id) {
        alert("dismiss " + id)
        $location.path("/tab/tasks")
    }

});
