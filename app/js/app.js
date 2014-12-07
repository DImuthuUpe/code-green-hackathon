// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.services' is found in services.js
// 'starter.controllers' is found in controllers.js
angular.module('starter', ['ionic', 'starter.controllers', 'starter.services'])

.run(function($rootScope,$http,$ionicPlatform) {
    
  $ionicPlatform.ready(function() {
     $rootScope.host = "http://umkkeb295ebf.madytyoo.koding.io:8081"
     $rootScope.pubnub  = PUBNUB.init({
          publish_key: 'pub-c-55cf3b7d-b27b-478a-99f3-158762ffcf86',
          subscribe_key: 'sub-c-1c9e1394-7a15-11e4-82cc-02ee2ddab7fe'
        });

      
    if(window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
})

.config(function($stateProvider, $urlRouterProvider) {

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider
    // setup an abstract state for the tabs directive
    .state('tab', {
      url: "/tab",
      abstract: true,
      templateUrl: "templates/tabs.html"
    })

    // Each tab has its own nav history stack:

    .state('tab.home', {
      url: '/home',
      views: {
        'tab-home': {
          templateUrl: 'templates/tab-home.html',
          controller: 'HomeCtrl'
        }
      }
    })
    .state('tab.select', {
      url: '/select',
      views: {
        'tab-home': {
          templateUrl: 'templates/tab-select.html',
          controller: 'SelectCtrl'
        }
      }
    })
    .state('tab.good', {
      url: '/good/:score',
      views: {
        'tab-home': {
          templateUrl: 'templates/good.html',
          controller: 'ResultCtrl'
        }
      }
    })
    .state('tab.bad', {
      url: '/bad/:score',
      views: {
        'tab-home': {
          templateUrl: 'templates/bad.html',
          controller: 'ResultCtrl'
        }
      }
    })
    
    .state('tab.stats', {
      url: '/stats',
      views: {
        'tab-stats': {
          templateUrl: 'templates/tab-stats.html',
          controller: 'StatsCtrl'
        }
      }
    })
    .state('tab.tasks', {
      url: '/tasks',
      views: {
        'tab-tasks': {
          templateUrl: 'templates/tab-tasks.html',
          controller: 'TasksCtrl'
        }
      }
    })
    .state('intro', { url: '/', templateUrl: 'templates/intro.html', controller: 'IntroCtrl' })
    .state('register', { url: '/register', templateUrl: 'templates/register.html', controller: 'RegisterCtrl' })
  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/');

});

