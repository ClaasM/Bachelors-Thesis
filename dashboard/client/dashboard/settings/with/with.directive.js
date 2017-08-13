/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('with', function () {
  return {
    templateUrl: './dashboard/settings/with/with.html',
    restrict: 'E',
    scope: {
      settings: '=settings'
    },
    link: function (scope, element, attrs) {
    }
  }
});