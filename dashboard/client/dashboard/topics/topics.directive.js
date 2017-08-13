/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('topics', function () {
  return {
    templateUrl: './dashboard/topics/topics.html',
    restrict: 'E',
    scope: {
      data: '=data'
    },
    link: function (scope, element, attrs) {
      scope.data = {};

      google.charts.load('current', {'packages': ['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Time', 'iPhone', 'release', 'Release'],
          [1, 90, 5, 5],
          [2, 90, 4, 6],
          [3, 91, 5, 4],
          [4, 88, 6, 6]
        ]);

        var options = {
          title: 'Top 3 LDA Keywords',
          hAxis: {title: 'Time since measurement', titleTextStyle: {color: '#333'}},
          isStacked: 'relative',
          height: 300,
          legend: {position: 'top', maxLines: 3},
          vAxis: {
            minValue: 0,
            ticks: [0, .3, .6, .9, 1] //TODO do this on the hAxis with [-window:0]
          }
        };

        var chart = new google.visualization.AreaChart(document.getElementById('topics_chart'));
        chart.draw(data, options);
      }


    }
  }
});