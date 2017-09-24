'use strict';

angular.module('Dashboard', [
  'ngCookies',
  'ngRoute'])
    .config(
        function ($routeProvider, $locationProvider, $httpProvider) {
          $routeProvider
              .when('/', {
                templateUrl: '/main/main.html',
                controller: 'MainCtrl'
              })
              .when('/dashboard', {
                templateUrl: '/dashboard/dashboard.html',
                controller: 'DashboardCtrl'
              })
              .otherwise({
                redirectTo: '/'
              });
          $locationProvider.html5Mode(true);
          //$httpProvider.interceptors.push('authInterceptor');
        })
    .filter('reverse', function () {
      return function (items) {
        if(!items) return items;
        return items.slice().reverse();
      };
    });


google.charts.load('current', {'packages': ['corechart']});