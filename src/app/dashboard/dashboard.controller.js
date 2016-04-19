(function() {
    'use strict';
    
    angular
        .module('app.dashboard')
        .controller('DashboardController', DashboardController);
    
    DashboardController.$inject = ['partyService', 'user'];
    
    function DashboardController(partyService, user) {
        var vm = this;

        vm.parties = partyService.getPartiesByUser(user.uid);
    }
    
})();