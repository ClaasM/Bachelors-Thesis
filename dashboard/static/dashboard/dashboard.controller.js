/**
 * Created by claasmeiners on 31/07/17.
 */
'use strict';

angular.module('Dashboard')
    .controller('DashboardCtrl', function ($scope, $http) {










      //Dummy Data
      $scope.data = {
        topics: [
          {
            text: "iPhone",
            value: 0.8
          }, {
            text: "iPad",
            value: 0.5
          }, {
            text: "iMac",
            value: 0.2
          }
        ],
        sentiment: [
          {
            text: "Anger",
            value: 0.8
          }, {
            text: "Happiness",
            value: 0.5
          }
        ],
        tweets: [
          {
            text: "Tweet 1"
          }, {
            text: "Tweet 2"
          }
        ]
      }
    });