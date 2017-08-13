/**
 * Created by claasmeiners on 13/08/17.
 */
angular.module('Dashboard').directive('sentiment', function () {
  return {
    templateUrl: './dashboard/sentiment/sentiment.html',
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
          ['Time', '', '', ''],
          [1, 0, 0, 0],
          [2, 0, 0, 0],
          [3, 0, 0, 0],
          [4,0, 0, 0]
        ]);

        var options = {
          title: 'Sentiment Analysis',
          hAxis: {title: 'Time since measurement', titleTextStyle: {color: '#333'}},
          isStacked: 'relative',
          height: 300,
          legend: {position: 'top', maxLines: 3},
          vAxis: {
            minValue: 0,
            ticks: [0, .3, .6, .9, 1] //TODO do this on the hAxis with [-window:0]
          }
        };

        var chart = new google.visualization.AreaChart(document.getElementById('sentiment_chart'));
        chart.draw(data, options);
      }


    }
  }
});