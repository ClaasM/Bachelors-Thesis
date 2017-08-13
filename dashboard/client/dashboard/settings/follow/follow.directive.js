/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('follow', function () {
  return {
    templateUrl: './dashboard/follow/follow.html',
    restrict: 'E',
    scope: {
      settings: '=settings'
    },
    link: function (scope, element, attrs) {
    }
  }
});