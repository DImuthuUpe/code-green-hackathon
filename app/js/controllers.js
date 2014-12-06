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
    $scope.register = function(id) {
        alert("id:" + id)
    }
    
})
.controller('DashCtrl', function($scope,$rootScope,$location) {
    if(!$rootScope.in) {
        alert("not in")
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
