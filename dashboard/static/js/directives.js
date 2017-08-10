'use strict';

/* Directives */

angular.module('Dashboard').directive('stringList', function () {
  return {
    templateUrl: 'static/dashboard/stringList/stringList.html',
    restrict: 'E',
    scope: {
      array: '=array'
    },
    link: function (scope, element, attrs) {
    }
  }
});