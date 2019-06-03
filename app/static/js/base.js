;(function($){
    'use strict';

    function setUserResources($btn, data, $userResources) {
        for (let resource in data.added_resource){
            let resource_amount = $userResources.data('army-'+resource);
            console.log(data.added_resource[resource]['amount']);
            $('#current-'+resource+'-amount').text(resource_amount + data.added_resource[resource]['amount']);
            $('#user-resources').data(`army-${resource}` ,resource_amount + data.added_resource[resource]['amount'])
        }
        $btn.data('turns-amount', data.turnsAmount);
        $('#current-turns-amount').text('turns: '+data.turnsAmount);
    }

    function setCardBody($btn, added_resource) {
        let $card_body = $btn.closest('.card').find('.card-body');
        $card_body.empty();
        $card_body.append('<h5 class="card-title">Search for resources</h5>');
        $card_body.append('<p class="card-text"> you found: </p><div class="d-flex"></div>');
        for (let resource in added_resource) {
            $card_body.find('div').append('<div class="col text-center mt-2"></div>');
            $card_body.find('.col').last().append(`<p class="card-text mb-0"><img class="resource-img img-fluid" src="${added_resource[resource]['picture']}" /></p>`);
            $card_body.find('.col').last().append(`<p class="card-text">${added_resource[resource]['amount']}</p>`);
        }
    }

    function setupResourceSearch() {
        $('#search-resources-btn').on('click', function(){
            let $btn = $(this),
                $userResources = $('#user-resources'),
                turnsAmount = $btn.data('turns-amount');

            if (turnsAmount < 10)
                return false

            $.gameApiPost('base/search_resources',{}).done(function(data){
                setUserResources($btn, data, $userResources);
                setCardBody($btn, data.added_resource);
            });
        });
    }
    setupResourceSearch();
}(jQuery));