/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('track', function () {
  return {
    templateUrl: './dashboard/track/track.html',
    restrict: 'E',
    scope: {
      settings: '=settings'
    },
    link: function (scope, element, attrs) {
    }
  }
});