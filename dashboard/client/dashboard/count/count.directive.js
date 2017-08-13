/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('count', function () {
  return {
    templateUrl: './dashboard/count/count.html',
    restrict: 'E',
    scope: {
      settings: '=settings'
    },
    link: function (scope, element, attrs) {
    }
  }
});