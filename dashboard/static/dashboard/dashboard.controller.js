/**
 * Created by claasmeiners on 31/07/17.
 */
'use strict';

angular.module('Dashboard')
    .controller('DashboardCtrl', function ($scope, $http) {

      var number_of_tweets_shown = 4;

      var socket = io();
      socket.on('dashboard.direct_message-create', function (data) {
        console.log(data);
      });
      socket.on('dashboard.friends-create', function (data) {
        console.log(data);
      });
      socket.on('dashboard.event-create', function (data) {
        console.log(data);
      });

      socket.on('dashboard.status-create', function (data) {
        console.log(data);
        _(number_of_tweets_shown).times(function (index) {
          $scope.data.tweets[number_of_tweets_shown - index] = $scope.data.tweets[number_of_tweets_shown - index - 1];
        });
        $scope.data.tweets[0] = {
          text: data.text,
          name: data.user.name
        };
        //TODO use ngSocket
        $scope.$digest()
      });


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
        tweets: []
      }
    });