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
}).directive('locationList', function () {
  return {
    templateUrl: 'static/dashboard/locationList/locationList.html',
    restrict: 'E',
    scope: {
      array: '=array'
    },
    link: function (scope, element, attrs) {
      scope.newLocation = [];

      scope.stepRange = function (max, step) {
        var input = [];
        for (var i = 0; i < max; i += step) {
          input.push(i);
        }
        return input;
      };
    }
  }
}).directive('languageSelect', function () {
  return {
    templateUrl: 'static/dashboard/locationList/locationList.html',
    restrict: 'E',
    scope: {
      array: '=array'
    },
    link: function (scope, element, attrs) {
      scope.languages = ["de", "en"];
      //TODO there are to many bcp 47 languages
    }
  }
});