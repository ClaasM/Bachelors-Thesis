/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('topics', function () {
  return {
    templateUrl: './dashboard/topics/topics.html',
    restrict: 'E',
    scope: {
      results: '=results'
    },
    link: function (scope, element, attrs) {


    }
  }
});