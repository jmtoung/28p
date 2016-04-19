(function() {
    'use strict';
    
    angular
        .module('app.dashboard')
        .directive('gzPartyTable', gzPartyTable);
    
    function gzPartyTable() {
        return {
            templateUrl: 'app/dashboard/directives/partyTable.html',
            restrict: 'E',
            controller: PartyTableController,
            controllerAs: 'vm',
            bindToController: true,
            scope: {
                parties: '='
            }
        };
    }
    
    PartyTableController.$inject = ['textMessageService'];
    
    function PartyTableController(textMessageService) {
        var vm = this;
        
        vm.removeParty = removeParty;
        vm.sendTextMessage = sendTextMessage;
        vm.toggleDone = toggleDone;

        function removeParty(party) {
            vm.parties.$remove(party);
        }

        function sendTextMessage(party) {
            textMessageService.sendTextMessage(party, vm.parties);
        }

        function toggleDone(party) {
            vm.parties.$save(party);
        }
    }

})();