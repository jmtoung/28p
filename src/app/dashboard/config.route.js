(function() {
    'use strict';
    
    angular
        .module('app.dashboard')
        .config(configFunction)
    
    configFunction.$inject = ['$routeProvider'];
    
    function configFunction($routeProvider) {
        $routeProvider.when('/dashboard', {
            templateUrl: 'app/dashboard/dashboard.html',
            controller: 'DashboardController',
            controllerAs: 'vm',
            resolve: {user: resolveUser}
        });
    }
    
    resolveUser.$inject = ['authService'];
    
    function resolveUser(authService) {
        return authService.firebaseAuthObject.$requireAuth();    
    }
    
})();