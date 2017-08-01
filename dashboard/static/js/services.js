'use strict';

angular.module('dashboardServices', ['ngResource'])
    .factory('User', function UserResource($resource) {
      return $resource('/api/users/:id/:controller', {
        id: '@_id'
      }, {
        changePassword: {
          method: 'PUT',
          params: {
            controller: 'password'
          }
        },
        get: {
          method: 'GET',
          params: {
            id: 'me'
          }
        }
      });
    })
    .factory('authInterceptor', function ($rootScope, $q, $cookies, $location, Util) {
      return {
        // Add authorization token to headers
        request: function (config) {
          config.headers = config.headers || {};
          if ($cookies.get('token') && Util.isSameOrigin(config.url)) {
            config.headers.Authorization = 'Bearer ' + $cookies.get('token');
          }
          return config;
        },

        // Intercept 401s and redirect you to login
        responseError: function (response) {
          if (response.status === 401) {
            $location.path('/login');
            // remove any stale tokens
            $cookies.remove('token');
          }
          return $q.reject(response);
        }
      };
    })
    .factory('Auth', function ($location, $http, $cookies, $q, Util, User) {

      //TODO most of this isn't needed

      var safeCb = Util.safeCb;
      var currentUser = {};

      if ($cookies.get('token') && $location.path() !== '/logout') {
        currentUser = User.get();
      }

      var Auth = {

        /**
         * Authenticate user and save token
         *
         * @param  {Object}   user     - login info
         * @param  {Function} callback - optional, function(error, user)
         * @return {Promise}
         */
        login: function (user, callback) {
          return $http.post('/auth/local', {
            email: user.email,
            password: user.password
          })
              .then(function (res) {
                $cookies.put('token', res.data.token);
                currentUser = User.get();
                return currentUser.$promise;
              })
              .then(function (user) {
                safeCb(callback)(null, user);
                return user;
              })
              .catch(function () {
                Auth.logout();
                safeCb(callback)(err.data);
                return $q.reject(err.data);
              });
        },

        /**
         * Delete access token and user info
         */
        logout: function () {
          $cookies.remove('token');
          currentUser = {};
        },

        /**
         * Create a new user
         *
         * @param  {Object}   user     - user info
         * @param  {Function} callback - optional, function(error, user)
         * @return {Promise}
         */
        createUser: function (user, callback) {
          console.log("creating user");
          return User.save(user,
              function (data) {
                $cookies.put('token', data.token);
                currentUser = User.get();
                return safeCb(callback)(null, user);
              },
              function (err) {
                Auth.logout();
                return safeCb(callback)(err);
              }).$promise;
        },

        /**
         * Change password
         *
         * @param  {String}   oldPassword
         * @param  {String}   newPassword
         * @param  {Function} callback    - optional, function(error, user)
         * @return {Promise}
         */
        changePassword: function (oldPassword, newPassword, callback) {
          return User.changePassword({id: currentUser._id}, {
            oldPassword: oldPassword,
            newPassword: newPassword
          }, function () {
            return safeCb(callback)(null);
          }, function (err) {
            return safeCb(callback)(err);
          }).$promise;
        },

        /**
         * Gets all available info on a user
         *   (synchronous|asynchronous)
         *
         * @param  {Function|*} callback - optional, funciton(user)
         * @return {Object|Promise}
         */
        getCurrentUser: function (callback) {
          if (arguments.length === 0) {
            return currentUser;
          }

          var value = (currentUser.hasOwnProperty('$promise')) ?
              currentUser.$promise : currentUser;
          return $q.when(value)
              .then(function (user) {
                    safeCb(callback)(user);
                    return user;
                  }, function () {
                    safeCb(callback)({});
                    return {};
                  }
              )
              ;
        },

        /**
         * Check if a user is logged in
         *   (synchronous|asynchronous)
         *
         * @param  {Function|*} callback - optional, function(is)
         * @return {Bool|Promise}
         */
        isLoggedIn: function (callback) {
          if (arguments.length === 0) {
            return currentUser.hasOwnProperty('role');
          }

          return Auth.getCurrentUser(null)
              .then(function (user) {
                var is = user.hasOwnProperty('role');
                safeCb(callback)(is);
                return is;
              })
              ;
        },

        /**
         * Get auth token
         *
         * @return {String} - a token string used for authenticating
         */
        getToken: function () {
          return $cookies.get('token');
        }
      };
      return Auth;
    })
    .factory('Util', function ($window) {
      var Util = {
        /**
         * Return a callback or noop function
         *
         * @param  {Function|*} cb - a 'potential' function
         * @return {Function}
         */
        safeCb: function (cb) {
          return (angular.isFunction(cb)) ? cb : angular.noop;
        },

        /**
         * Parse a given url with the use of an anchor element
         *
         * @param  {String} url - the url to parse
         * @return {Object}     - the parsed url, anchor element
         */
        urlParse: function (url) {
          var a = document.createElement('a');
          a.href = url;
          return a;
        },

        /**
         * Test whether or not a given url is same origin
         *
         * @param  {String}           url       - url to test
         * @param  {String|String[]}  [origins] - additional origins to test against
         * @return {Boolean}                    - true if url is same origin
         */
        isSameOrigin: function (url, origins) {
          url = Util.urlParse(url);
          origins = (origins && [].concat(origins)) || [];
          origins = origins.map(Util.urlParse);
          origins.push($window.location);
          origins = origins.filter(function (o) {
            return url.hostname === o.hostname &&
                url.port === o.port &&
                url.protocol === o.protocol;
          });
          return (origins.length >= 1);
        }
      };

      return Util;
    });




