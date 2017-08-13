/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('replies', function () {
  return {
    templateUrl: './dashboard/replies/replies.html',
    restrict: 'E',
    scope: {
      settings: '=settings'
    },
    link: function (scope, element, attrs) {
    }
  }
});