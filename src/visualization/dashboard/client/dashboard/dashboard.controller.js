/**
 * Created by claasmeiners on 31/07/17.
 */
'use strict';

angular.module('Dashboard')
    .controller('DashboardCtrl', function ($scope, $http) {
      $scope.isStreaming = false;
      $scope.isLoading = false;
      $scope.selectedStream = 'public';
      $scope.streamSettings = {
        'user': {
          type: 'user',
          _with: 'followings',
          replies: 'all',
          track: [],
          locations: []
        },
        'site': {
          type: 'site',
          _with: 'followings',
          replies: 'all',
          follow: []
        },
        /* TODO rename */
        'public': {
          type: 'public',
          'filter_level': 'none',
          follow: [],
          track: ['iphone'],
          locations: [],
          languages: []
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
      var RESULTS_DEFAULT = {
        tweets: [],
        wordcount: []
      };
      $scope.results = RESULTS_DEFAULT;

      var socket = io();
      $scope.updateSettings = function () {
        console.log($scope.streamSettings[$scope.selectedStream]);
        socket.emit('dashboard.update', $scope.streamSettings[$scope.selectedStream]);
        $scope.isLoading = true;
        $scope.isStreaming = false;
      };

      socket.on('dashboard.update-success', function () {
        //This is emitted by the server if the update was successful
        $scope.isStreaming = true;
        $scope.isLoading = false;
        //Reset the dashboard
        $scope.results = RESULTS_DEFAULT;
      });

      socket.on('dashboard.update-error', function () {
        //TODO This is emitted by the server if the update was not successful

      });

      socket.on('dashboard.wordcount-update', function (data) {
        $scope.results.wordcount = data;
        //TODO use ngSocket
        $scope.$digest()
      });


      //Number of tweets shown in the tweets-column of the dashboard
      var MAX_NUMBER_OF_TWEETS_SHOWN = 4;
      socket.on('dashboard.status-create', function (data) {

        //console.log(data);
        var number_of_tweets_shown = Math.min(MAX_NUMBER_OF_TWEETS_SHOWN, $scope.results.tweets.length + 1);
        _(number_of_tweets_shown).times(function (index) {
          $scope.results.tweets[number_of_tweets_shown - index] = $scope.results.tweets[number_of_tweets_shown - index - 1];
        });
        $scope.results.tweets[0] = {
          text: data.text,
          name: data.user.name
        };
        //TODO use ngSocket
        $scope.$digest()
      });


      socket.on('dashboard.direct_message-create', function (data) {
        console.log(data);
      });
      socket.on('dashboard.friends-create', function (data) {
        console.log(data);
      });
      socket.on('dashboard.event-create', function (data) {
        console.log(data);
      });
      /**
       * TODO this can be removed if the other thing works
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