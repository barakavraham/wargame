;(function($){
    'use strict';

    $(function() {

        let $techBtn = $('.tech-btn'),
            $tableContainer = $('.table-container'),
            $userResources = $('#user-resources');

        function setupSwitchTables() {
            $techBtn.on('click', function() {
                $tableContainer.find('table').hide();
                $tableContainer.find('table').next('table').show();
            });

            $('.weapon-btn').on('click', function() {
                $tableContainer.find('table').next('table').hide();
                $tableContainer.find('table').first().show();
            });
        }

        function canBuy($btn, amount = 1) {
            for (let resource in $btn.data()) {
                let formattedResource = resource.replace('cost', '').toLowerCase(),
                    resourceAmount = $userResources.data('army-'+formattedResource);
                if (resourceAmount && resourceAmount < ($btn.data(resource) * amount)) {
                    return false;
                }
            }
            return true;
        }

        function setUserResources($btn, amount = 1) {
            for (let resource in $btn.data()) {
                if (_.includes(resource, 'cost')) {
                    let formattedResource = resource.replace('cost', '').toLowerCase(),
                        resourceCost = $btn.data(resource),
                        currentResourceAmount = $userResources.data('army-'+formattedResource);
                    $('#current-'+formattedResource+'-amount').text(currentResourceAmount - resourceCost * amount);
                    $userResources.data('army-'+formattedResource, currentResourceAmount - resourceCost * amount);
                }
            }
        }

        function setButtonPrices($btn, prices) {
            if (prices) {
                $btn.closest('tr').find('.td-item-cost').empty();
                for (let resource in prices) {
                    $btn.closest('tr').find('.td-item-cost').append("<div></div>");
                    $btn.closest('tr').find('.td-item-cost').find('div').last()
                        .append(`<h5 class='item-cost ${resource}-price'></h5>`)
                        .append(`<img class="img ${resource}-img"  src="${prices[resource]['picture']}"></img>`);
                    $btn.data('cost-'+resource, prices[resource]['price']);
                    $btn.closest('tr').find('.'+resource+'-price').text(prices[resource]['price']);
                }
            } else {
                console.log('maxed out');
                $btn.closest('tr').find('.td-item-cost').empty();
                $btn.closest('tr').find('.td-item-cost').append("<div></div>");
                $btn.closest('tr').find('.td-item-cost').find('div').last()
                .append("<h5 class='item-cost'> You have reached to the max level </h5>");
                $btn.closest('tr').find('.current-level').text('max');
                $btn.remove();
            }
        }

        function setupBuyResources() {
            $('.amount').on('input', function() {
                $(this).val($(this).val().replace(/\D/g, ''));
            });

            $('.buy-btn').on('click', function() {
                let $buyBtn = $(this),
                    $purchaseResult = $buyBtn.next('div.purchase-result'),
                    $amountInput = $buyBtn.prev('.amount'),
                    amount = Number($amountInput.val()),
                    currentResourceAmount = Number($buyBtn.closest('tr').find('.current-amount').text());

                $('div.purchase-result').text('');
                $purchaseResult.removeClass('success, fail');
                $purchaseResult.text('');

                if (amount <= 0) {
                    $amountInput.val('');
                    $purchaseResult.addClass('fail').text('Please enter a valid amount');
                    return false;
                }

                if (!canBuy($buyBtn, amount)) {
                    $purchaseResult.addClass('fail').text('Not enough resources');
                    return false;
                }

                $.gameApiPost('shop/buy_resources', {
                    item: $buyBtn.data('item'),
                    amount: amount
                }).done(function() {
                    $buyBtn.closest('tr').find('.current-amount').text(currentResourceAmount + amount);
                    setUserResources($buyBtn);
                    $purchaseResult.addClass('success').text('Purchase successful');
                    $amountInput.val('');
                }).fail(function({ status }) {
                    if (status === 400)
                        $purchaseResult.addClass('fail').text('Not enough resources');
                })
            });
        }

        function setupTechUpgrades() {
            $('.upgrade-btn').on('click', function() {
                let $upgradeBtn = $(this),
                    nextUpgradeLevel = $upgradeBtn.data('next-level'),
                    $purchaseResult = $upgradeBtn.next('div.purchase-result');

                $('div.purchase-result').text('');
                $purchaseResult.removeClass('success, fail');
                $purchaseResult.text('');

                if (!canBuy($upgradeBtn)) {
                    $purchaseResult.addClass('fail').text('Not enough resources');
                    return false;
                }

                $.gameApiPost('shop/upgrade', {
                    upgrade: $upgradeBtn.data('item-upgrade'),
                    level: nextUpgradeLevel
                }).done(function(data) {
                    setUserResources($upgradeBtn);
                    if (nextUpgradeLevel < 5)
                        $upgradeBtn.closest('tr').find('.current-level').text(nextUpgradeLevel);
                    $upgradeBtn.data('next-level', nextUpgradeLevel + 1);
                    if (data.picture)
                        $upgradeBtn.closest('tr').find('.wep-img').attr('src', data.picture['picture']);

                    setButtonPrices($upgradeBtn, data.prices);

                    $purchaseResult.addClass('success').text('Purchase successful');
                }).fail(function({ status, max_level }) {
                    if (status === 400)
                        $purchaseResult.addClass('fail').text('Not enough resources');
                    else if (max_level)
                        $purchaseResult.addClass('fail').text('200');
                })
            });
        }


        setupSwitchTables();
        setupBuyResources();
        setupTechUpgrades();

    });
}(jQuery));

