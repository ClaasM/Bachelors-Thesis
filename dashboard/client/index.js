'use strict';

angular.module('Dashboard', ['dashboardServices',
  'ngCookies',
  'ngRoute'])
    .config(
        function ($routeProvider, $locationProvider, $httpProvider) {
          $routeProvider
              .when('/', {
                templateUrl: '..//main/main.html',
                controller: 'MainCtrl'
              })
              .when('/dashboard', {
                templateUrl: '..//dashboard/dashboard.html',
                controller: 'DashboardCtrl'
              })
              .otherwise({
                redirectTo: '/'
              });
          $locationProvider.html5Mode(true);
          //$httpProvider.interceptors.push('authInterceptor');
        })
    .run(function ($rootScope, $location, Auth) {
      // Redirect to login if route requires auth and the user is not logged in, or doesn't have required role
      $rootScope.$on('$routeChangeStart', function (event, next) {
        if (!next.authenticate) {
          return;
        }

        if (typeof next.authenticate === 'string') {
          Auth.hasRole(next.authenticate, _.noop).then(function (has) {
            if (has) {
              return;
            }

            event.preventDefault();
            return Auth.isLoggedIn(_.noop).then(function (is) {
              $location.path(is ? '/' : '/login');
            })
                ;
          });
        } else {
          Auth.isLoggedIn(_.noop).then(function (is) {
            if (is) {
              return;
            }

            event.preventDefault();
            $location.path('/');
          });
        }
      });
    });