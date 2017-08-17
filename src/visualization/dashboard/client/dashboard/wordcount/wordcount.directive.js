/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('wordcount', function () {
  return {
    templateUrl: './dashboard/wordcount/wordcount.html',
    restrict: 'E',
    scope: {
      results: '=results'
    },
    link: function (scope, element, attrs) {

    }
  }
});