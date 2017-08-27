/**
 * Created by claasmeiners on 31/07/17.
 * The Main Dashboard controller.
 * Receives the updates from the backend and updates the results-object on the scope accordingly.
 */
'use strict';

angular.module('Dashboard')
    .controller('DashboardCtrl', function ($scope, $http) {
      // Used to visualize what is currently happening
      $scope.isStreaming = false;
      $scope.isLoading = false;
      //The default selected stream
      $scope.selectedStream = 'public';
      //The default stream setting
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
          languages: ['en']
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
      // Number of tweets shown in the recent tweets-part
      var MAX_NUMBER_OF_TWEETS_SHOWN = 4;
      var RESULTS_DEFAULT = {
        tweets: [],
        wordcount: [],
        topics: [],
        emotion: {
          positive: 0,
          negative: 0
        }
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

      //Called whenever a new tweet arrives via the stream, is analyzed and then sent to the client
      socket.on('dashboard.update', function (data) {
        console.log(data);
        //Update the emotion scores
        $scope.results.emotion.positive += data.emotion.positive;
        $scope.results.emotion.negative += data.emotion.negative;

        //Update the topics probabilities
        _.forEach(data.topics, function (value, key) {
          if ($scope.results.topics[key]) {
            $scope.results.topics[key].probability += value.probability
          } else {
            $scope.results.topics[key] = value
          }
        });

        //Show the new tweet
        var number_of_tweets_shown = Math.min(MAX_NUMBER_OF_TWEETS_SHOWN, $scope.results.tweets.length + 1);
        _(number_of_tweets_shown).times(function (index) {
          $scope.results.tweets[number_of_tweets_shown - index] = $scope.results.tweets[number_of_tweets_shown - index - 1];
        });
        $scope.results.tweets[0] = {
          text: data.tweet.text,
          name: data.tweet.user.name
        };

        //Perform a angular digest so that the changes are represented in the DOM
        $scope.$digest()
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