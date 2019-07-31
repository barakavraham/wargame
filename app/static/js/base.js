;(function($){
    'use strict';

    $(function() {
        let $userResources = $('#user-resources'),
            $searchResourcesBtn = $('#search-resources-btn'),
            $searchFieldBtn = $('#search-field-btn'),
            $currentTurnsAmount = $('#current-turns-amount');
    

        function setUserResources({ added_resources, turns }, $userResources) {
            for (let resource in added_resources){
                let resource_amount = $userResources.data('army-'+resource);
                $(`#current-${resource}-amount`).text(numberWithCommas(resource_amount + added_resources[resource].amount));
                $userResources.data(`army-${resource}` ,resource_amount + added_resources[resource].amount);
            }
            $userResources.data('army-turns', turns);
            $currentTurnsAmount.text(`turns: ${turns}`);
        }

        function setCardBody($btn, { added_resources }) {
            let $card_body = $btn.closest('.card').find('.card-body');
            $card_body.empty();
            if (added_resources['field'])
                $card_body.append('<h5 class="card-title">Search for field</h5>');
            else
                $card_body.append('<h5 class="card-title">Search for resources</h5>');
            $card_body.append('<p class="card-text"> you found: </p><div class="d-flex resources-div"></div>');
            for (let resource in added_resources) {
                if (resource === 'diamond')
                    $card_body.append('<div class="d-flex resources-div mt-3"></div>');
                var sNumber = numberWithCommas(added_resources[resource].amount);
                $card_body.find('.resources-div').last().append('<div class="col text-center"></div>');
                $card_body.find('.col').last().append(`<p class="card-text"><img class="resource-img img-fluid" src="${added_resources[resource].picture}" /></p>`);
                $card_body.find('.col').last().append(`<div class="wrapper">
                                                         <div class="letters"> 
                                                          <div class="numbers mt-2">
                                                        </div></div></div>`);

                for (var i = 0, len = sNumber.length; i < len; i += 1) {
                    $card_body.find('.col').last().find('.numbers').last().append(`<span class="letter"> ${sNumber.charAt(i)}`);
                }
            }
        }

        function setPurchaseResultsMessage($purchaseResultsDiv, purchaseSuccess, text) {
            $purchaseResultsDiv.removeClass('message-showing').empty();
            $purchaseResultsDiv.append(`<p>${text}</p>`).addClass('message-showing');
            $purchaseResultsDiv.find('p').addClass(purchaseSuccess ? 'bg-success' : 'bg-warning');
            setTimeout(function() {
                $purchaseResultsDiv.removeClass('message-showing');
            }, 2000)
        }

        function setupResourceSearch() {
            $searchResourcesBtn.on('click', function(){
                let $btn = $(this),
                    $purchaseResult = $btn.closest('.card').find('.purchase-result'),
                    turns = $userResources.data('army-turns'),
                    purchaseSuccess = false;

                if (turns < 10) {
                    setPurchaseResultsMessage($purchaseResult, purchaseSuccess, "You don't have enough turns");
                    return false;
                }

                $.gameApiGet('base/search_resources').done(function(user_new_resources){
                    setCardBody($btn, user_new_resources);
                    $btn.prop('disabled', true);
                    setTimeout(function(){
                        $btn.prop('disabled', false);
                        setUserResources(user_new_resources, $userResources); // resources will update only after the spin //
                    }, 2000);

                }).fail(function({ status }){
                    setPurchaseResultsMessage($purchaseResult, purchaseSuccess, status === 400 ? "You don't have enough turns" : 'An error occurred');
                })
            });
        }

        function setupFieldSearch() {
            $searchFieldBtn.on('click', function(){
                let $btn = $(this),
                    $purchaseResult = $btn.closest('.card').find('.purchase-result'),
                    turns = $userResources.data('army-turns'),
                    purchaseSuccess = false;

                if (turns < 15) {
                    setPurchaseResultsMessage($purchaseResult, purchaseSuccess, "You don't have enough turns");
                    return false;
                }

                $.gameApiGet('base/search_field').done(function(user_new_field){
                    setCardBody($btn, user_new_field);
                    $btn.prop('disabled', true);
                    setTimeout(function(){
                        $btn.prop('disabled', false);
                        setUserResources(user_new_field, $userResources); // resources will update only after the spin //
                    }, 2000);
                }).fail(function({ status }){
                    setPurchaseResultsMessage($purchaseResult, purchaseSuccess, status === 400 ? "You don't have enough turns" : 'An error occurred');
                });
            });
        }

        setupResourceSearch();
        setupFieldSearch()
        
    });
}(jQuery));
