'use strict';

/* Filters */

angular.module('dashboardFilters', []).filter('uppercase', function() {
	return function(input) {
		return input.toUpperCase();
	}
});