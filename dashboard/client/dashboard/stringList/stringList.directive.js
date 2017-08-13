/**
 * Created by claasmeiners on 13/08/17.
 */

angular.module('Dashboard').directive('stringList', function () {
  return {
    templateUrl: './dashboard/stringList/stringList.html',
    restrict: 'E',
    scope: {
      array: '=array'
    },
    link: function (scope, element, attrs) {
    }
  }
});