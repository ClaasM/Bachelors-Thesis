/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('languages', function () {
  return {
    templateUrl: './dashboard/settings/languages/languages.html',
    restrict: 'E',
    scope: {
      settings: '=settings'
    },
    link: function (scope, element, attrs) {
    }
  }
});