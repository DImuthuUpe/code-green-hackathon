angular.module('starter.controllers', ['ngCookies'])

.controller('IntroCtrl', function($scope,$rootScope,$http,$cookies) {
        $rootScope.in = false;
         $scope.nextPage = '#/tab/dash';
         var user = $cookies.puppyEarth;    
         
         if( user == undefined) {
             $scope.nextPage = '#/register';
         } else {
            $http.get($rootScope.host+"/ping")
            .success(function (data) {
                alert(data)
            }).error(function () {
                alert("error")
            });
             
         }
         
        

})

.controller('RegisterCtrl', function($scope,$rootScope, $http,$timeout) {
    $scope.countries = []
    $timeout(function() {
    $http.get($rootScope.host+"/")
        .success(function (data) {
            $scope.countries = data
        })
        
    },100)
    $scope.register = function(country) {
        var xsrf = { country: country };
        $http({
                method: 'POST',
                url: $rootScope.host+"/register",
                data: xsrf,
            }).success(function () {
                alert("yess")
            }).error(function() {
                alert("Error")
            })
    }
    
})
.controller('DashCtrl', function($scope,$rootScope,$location) {
    if(!$rootScope.in) {
        $location.path("/")
    }
})

.controller('FriendsCtrl', function($scope,$rootScope, $http) {
  $scope.friends = []
      $http.get($rootScope.host+"/")
        .success(function (data) {
            $scope.friends = data
        }).error(function () {
            alert("error")
        });

})

.controller('FriendDetailCtrl', function($scope, $stateParams, Friends) {
  $scope.friend = Friends.get($stateParams.friendId);
})

.controller('AccountCtrl', function($scope) {
});
