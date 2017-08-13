/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('filterLevel', function () {
  return {
    templateUrl: './dashboard/filterLevel/filterLevel.html',
    restrict: 'E',
    scope: {
      settings: '=settings'
    },
    link: function (scope, element, attrs) {
    }
  }
});