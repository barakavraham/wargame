;(function($){
    'use strict';

    $(function() {
        let $userResources = $('#user-resources');
    

        function setUserResources({ added_resource, turns }, $userResources) {
            for (let resource in added_resource){
                let resource_amount = $userResources.data('army-'+resource);
                $(`#current-${resource}-amount`).text(resource_amount + added_resource[resource].amount);
                $('#user-resources').data(`army-${resource}` ,resource_amount + added_resource[resource].amount);
            }
            $userResources.data('army-turns', turns);
            $('#current-turns-amount').text(`turns: ${turns}`);
        }

        function setSpinner($btn, {added_resource}) {
            let $card_body = $btn.closest('.card').find('.card-body');
            $card_body.empty();
            if (added_resource['field'])
                $card_body.append('<h5 class="card-title">Search for field</h5>');
            else
                $card_body.append('<h5 class="card-title">Search for resources</h5>');
            $card_body.append(`<div class="spinner">
                                <div class="rect1"></div>
                                <div class="rect2"></div>
                                <div class="rect3"></div>
                                <div class="rect4"></div>
                                <div class="rect5"></div>
                            </div>`);
            }

        function setCardBody($btn, {added_resource}) {
            let $card_body = $btn.closest('.card').find('.card-body');
            $card_body.empty();
            if (added_resource['field'])
                $card_body.append('<h5 class="card-title">Search for field</h5>');
            else
                $card_body.append('<h5 class="card-title">Search for resources</h5>');
            $card_body.append('<p class="card-text"> you found: </p><div class="d-flex"></div>');
            for (let resource in added_resource) {
                if (resource === 'diamond' && added_resource[resource].amount === 0)
                    continue;
                $card_body.find('div').append('<div class="col text-center mt-2 pl-0 pr-0"></div>');
                $card_body.find('.col').last().append(`<p class="card-text mb-0"><img class="resource-img img-fluid" src="${added_resource[resource].picture}" /></p>`);
                $card_body.find('.col').last().append(`<p class="card-text">${added_resource[resource].amount}</p>`);
            }
        }

        function setPurchaseResultsMessage($purchaseResultsDiv, purchaseSuccess, text) {
            $purchaseResultsDiv.removeClass('message-showing').empty();
            $purchaseResultsDiv.append(`<p>${text}</p>`).addClass('message-showing');
            if (purchaseSuccess)
                $purchaseResultsDiv.find('p').addClass('bg-success');
            else
                $purchaseResultsDiv.find('p').addClass('bg-warning');
            setTimeout(function() {
                $purchaseResultsDiv.removeClass('message-showing');
            }, 2000)
        }

        function setupResourceSearch() {
            $('#search-resources-btn').on('click', function(){
                let $btn = $(this),
                    $purchaseResult = $btn.closest('.card').find('.purchase-result'),
                    turns = $userResources.data('army-turns'),
                    purchaseSuccess = false;

                if (turns < 10) {
                    setPurchaseResultsMessage($purchaseResult, purchaseSuccess, "You don't have enough turns");
                    return false;
                }

                $.gameApiGet('base/search_resources').done(function(user_new_resources){
                    setSpinner($btn, user_new_resources);
                    setTimeout(function(){setUserResources(user_new_resources, $userResources)}, 3000);
                    setTimeout(function(){setCardBody($btn, user_new_resources)}, 3000);
                }).fail(function(status){
                    if (status === 400)
                        setPurchaseResultsMessage($purchaseResult, purchaseSuccess, "You don't have enough turns");
                    else
                        setPurchaseResultsMessage($purchaseResult, purchaseSuccess, "Status code");
                })
            });
        }

        function setupFieldSearch() {
            $('#search-field-btn').on('click', function(){
                let $btn = $(this),
                    $purchaseResult = $btn.closest('.card').find('.purchase-result'),
                    turns = $userResources.data('army-turns'),
                    purchaseSuccess = false;

                if (turns < 15) {
                    setPurchaseResultsMessage($purchaseResult, purchaseSuccess, "You don't have enough turns");
                    return false;
                }

                $.gameApiGet('base/search_field').done(function(user_new_field){
                    setSpinner($btn, user_new_field);
                    setTimeout(function(){setCardBody($btn, user_new_field)}, 3000);
                    setTimeout(function(){setUserResources(user_new_field, $userResources)}, 3000);
                }).fail(function({status}){
                    if (status === 400)
                        setPurchaseResultsMessage($purchaseResult, purchaseSuccess, "You don't have enough turns");
                    else
                        setPurchaseResultsMessage($purchaseResult, purchaseSuccess, 'Status code');
                });
            });
        }

        setupResourceSearch();
        setupFieldSearch()
        
    });
}(jQuery));
