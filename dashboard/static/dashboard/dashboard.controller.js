/**
 * Created by claasmeiners on 31/07/17.
 */
'use strict';

angular.module('Dashboard')
    .controller('DashboardCtrl', function ($scope, $http) {
      $scope.selectedStream = 'public';
      $scope.streamSettings = {
        'user': {
          type: 'user',
          _with: 'followings',
          replies: 'all',
          track: []
        },
        'site': {
          type: 'site'
        },
        /* TODO rename */
        'public': {
          type: 'public',
          'filter_level': 'none'
        },
        'sample': {
          type: 'sample'
        },
        'retweet': {
          type: 'retweet'
        },
        'firehose': {
          type: 'firehose',
          count: 0
        }
      };
      var socket = io();
      $scope.updateSettings = function () {
        console.log($scope.streamSettings[$scope.selectedStream]);
        //$http.post('/api/dashboard/update', $scope.streamSettings[$scope.selectedStream])
        socket.emit('update', $scope.streamSettings[$scope.selectedStream])
      };

      var number_of_tweets_shown = 4;


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

      /**
       * Sets or deletes a key on the streamSettings object.
       * This is useful since some parameters for the twitter streaming API are supposed to be either a specific string or nonexistent.
       * @param key the to set
       * @param value the value to set if it's not set already (in which case it's deleted)
       */
      $scope.setOrDelete = function (key, value) {
        if ($scope.streamSettings[key] == value) {
          delete $scope.streamSettings[$scope.selectedStream][key]
        } else {
          $scope.streamSettings[key] = value
        }
      }
    });