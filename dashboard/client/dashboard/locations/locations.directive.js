/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('locations', function () {
  return {
    templateUrl: './dashboard/locations/locations.html',
    restrict: 'E',
    scope: {
      settings: '=settings'
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
});