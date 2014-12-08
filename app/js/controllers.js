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
                    $scope.mood = "hungry.png"
                    
                } else {
                    $scope.mood = "bad2.png"
                    $timeout(function(){
                        $scope.mood = "healthy.png"
                    },(Math.floor(Math.random() * 200) + 1000))
                    
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
                    barColor: '#6FB3E0',
                    trackColor: '#E2E2E2',
                    scaleColor: false,
                    lineCap: 'butt',
                    lineWidth: 5,
                    animate: 1000,
                    size: 50
                });        
                
                 $('#tasks').data('easyPieChart').update($scope.total_tasks);
                
            })
})

.controller('StatsCtrl', function($scope,$rootScope, $http ,$cookies) {
    $scope.delta = 0    
    $scope.total_debit = 0 
    $scope.total_credit = 0
    $scope.image  = "up.png"
    $scope.target = 0
    var d = new Date();
    $http.get($rootScope.host+"/stats?registration=" + $cookies.puppyEarth + "&" + d.getTime() )
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
    $scope.index = 0
    $scope.food = []
    $scope.list = []
    
    $http.get($rootScope.host+"/foods")
        .success(function (data) {
             $scope.list  = data
             $timeout(function() {
                for (var i = 0; i < $scope.list.length; i++) {
                    $timeout(function () {
                        $scope.food.push( $scope.list[$scope.index++] );
                    }, 100 * i);
                };
            },200)

        })
        

    
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

.controller('ResultCtrl', function($scope,$stateParams, $http,$location,$timeout) {
    $scope.good = "healthy.png"
    $scope.bad = "bad" + (Math.floor(Math.random() * 3) + 1) + ".png"
    $scope.score = $stateParams.score
    $timeout(function(){
        $location.path( "/tab/home" )
    },3000)

    

}).controller('TasksCtrl', function($scope,$rootScope,$cookies,$http,$timeout) {
    $scope.index = 0
    $scope.tasks = []
    $scope.list = []
    
    $http.get($rootScope.host+"/task?registration=" + $cookies.puppyEarth )
        .success(function (data) {
            $scope.list = data;
            $timeout(function() {
                    for (var i = 0; i < $scope.list.length; i++) {
                        $timeout(function () {
                            $scope.tasks.push( $scope.list[$scope.index++] );
                        }, 100 * i);
                    };
                },200)
        })        
            
}).controller('TaskCtrl', function($scope,$rootScope,$stateParams, $http,$location) {
    $scope.task = {}
    
    $http.get($rootScope.host+"/tasks/" +  $stateParams.id )
        .success(function (data) {
            $scope.task = data;
        })
    
    
    $scope.complete = function(id) {
        $http.post( $rootScope.host + "/tasks/" + id + "/C", {  })
            .success(function (data) {
                $location.path("/tab/tasks")
            })
        
    }
    
    $scope.dismiss = function(id) {
        $http.post( $rootScope.host + "/tasks/" + id + "/D", {  })
            .success(function (data) {
                $location.path("/tab/tasks")
            })
    }

});
