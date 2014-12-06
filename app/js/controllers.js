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
            $location.path = "/home"
        })
        
    }
    
})
.controller('HomeCtrl', function($scope,$rootScope,$location) {
    //if(!$rootScope.in) {
    //    $location.path("/home")
    //}
})

.controller('StatsCtrl', function($scope,$rootScope, $http) {

})

.controller('FriendDetailCtrl', function($scope, $stateParams, Friends) {
  $scope.friend = Friends.get($stateParams.friendId);
})

.controller('TasksCtrl', function($scope) {
});
