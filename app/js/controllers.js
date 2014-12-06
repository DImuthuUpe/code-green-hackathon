angular.module('starter.controllers', [])

.controller('IntroCtrl', function($scope,$location) {
    $scope.start = function() {
        $location.path = "#/tab/dash"
    }
})

.controller('DashCtrl', function($scope) {
})

.controller('FriendsCtrl', function($scope, Friends) {
  $scope.friends = Friends.all();
})

.controller('FriendDetailCtrl', function($scope, $stateParams, Friends) {
  $scope.friend = Friends.get($stateParams.friendId);
})

.controller('AccountCtrl', function($scope) {
});
