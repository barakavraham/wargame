;(function($){
    'use strict';

    $(function() {

        let $techBtn = $('.tech-btn'),
            $techContainer = $('.upgrades-container'),
            $weaponBtn = $('.weapon-btn'),
            $weaponsContainer = $('.weapons-container'),
            $userResources = $('#user-resources');

        function setupSwitchTables() {
            $weaponBtn.on('click', function() {
                $techContainer.hide();
                $weaponsContainer.show();
            });

            $techBtn.on('click', function() {
                $weaponsContainer.hide();
                $techContainer.show();
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
            let $prices = $btn.parents('.card').find('.prices');
            $prices.empty();
            if (prices) {
                for (let resource in prices) {
                    $prices.append('<div class="col text-center mt-2"></div>');
                    let $resourceCol = $prices.find('.col').last();
                    $resourceCol.append(`<p class="card-text mb-0"><img class="resource-img img-fluid"  src="${prices[resource]['picture']}" /></p>`);
                    $resourceCol.append(`<p class="card-text">${prices[resource].price}</p>`);
                    $btn.data('cost-'+resource, prices[resource].price);
                }
            } else {
                $prices.append('<p class="col text-center">Maxed out</p>');
                $btn.remove();
            }
        }

        function setPurchaseResultsMessage($purchaseResultsDiv, purchaseSuccess, text) {
            $('div.purchase-result').removeClass('message-showing').empty();
            $purchaseResultsDiv.append(`<p>${text}</p>`).addClass('message-showing');
            if (purchaseSuccess)
                $purchaseResultsDiv.find('p').addClass('bg-success');
            else
                $purchaseResultsDiv.find('p').addClass('bg-warning');
            setTimeout(function() {
                $purchaseResultsDiv.removeClass('message-showing');
            }, 2000)
        }

        function setupBuyResources() {
            $('.amount').on('input', function() {
                $(this).val($(this).val().replace(/\D/g, ''));
            });

            $('.buy-btn').on('click', function() {
                let $buyBtn = $(this),
                    $purchaseResult = $buyBtn.closest('.weapon-container').find('div.purchase-result'),
                    $amountInput = $buyBtn.closest('.input-group').find('.amount'),
                    amount = Number($amountInput.val()),
                    currentResourceAmount = Number($buyBtn.closest('.weapon-container').find('.current-weapon-amount').text()),
                    purchaseSuccess = false;

                if (amount <= 0) {
                    $amountInput.val('');
                    setPurchaseResultsMessage($purchaseResult, false, 'Please enter a valid amount');
                    return false;
                }

                if (!canBuy($buyBtn, amount)) {
                    purchaseSuccess = false;
                    setPurchaseResultsMessage($purchaseResult, purchaseSuccess, 'Not enough resources');
                    return false
                } else
                    purchaseSuccess = true;

                $.gameApiPost('shop/buy_resources', {
                    item: $buyBtn.data('item'),
                    amount: amount
                }).done(function() {
                    setPurchaseResultsMessage($purchaseResult, true, 'Purchase successful');
                    $buyBtn.closest('.weapon-container').find('.current-weapon-amount').text(currentResourceAmount + amount);
                    setUserResources($buyBtn);
                    $amountInput.val('');
                }).fail(function({ status }) {
                    if (status === 400)
                        setPurchaseResultsMessage($purchaseResult, purchaseSuccess, 'Not enough resources');
                    else
                        setPurchaseResultsMessage($purchaseResult, purchaseSuccess, 'Status code');
                })
            });
        }

        function setupTechUpgrades() {
            $('.upgrade-btn').on('click', function() {
                let $upgradeBtn = $(this),
                    nextUpgradeLevel = $upgradeBtn.data('next-level'),
                    $purchaseResult = $upgradeBtn.closest('.upgrade-container').find('div.purchase-result'),
                    purchaseSuccess;

                if (!canBuy($upgradeBtn)) {
                    purchaseSuccess = false;
                    return false
                } else
                    purchaseSuccess = true;
                

                $.gameApiPost('shop/upgrade', {
                    upgrade: $upgradeBtn.data('item-upgrade'),
                    level: nextUpgradeLevel
                }).done(function(data) {
                    setPurchaseResultsMessage($purchaseResult, purchaseSuccess, 'Upgrade successful');
                    setUserResources($upgradeBtn);
                    if (nextUpgradeLevel < 5)
                        $upgradeBtn.closest('.upgrade-container').find('.current-upgrade-level').text(nextUpgradeLevel);
                    $upgradeBtn.data('next-level', nextUpgradeLevel + 1);
                    if (data.picture)
                        $upgradeBtn.closest('.upgrade-container').find('.card-img-top').attr('src', data.picture);
                    setButtonPrices($upgradeBtn, data.prices);
                }).fail(function({ status, max_level }) {
                    if (status === 400)
                        setPurchaseResultsMessage($purchaseResult, purchaseSuccess, 'Not enough resources')
                    else if (max_level)
                        $purchaseResult.addClass('bg-warning').text('200');
                    else
                        setPurchaseResultsMessage($purchaseResult, purchaseSuccess, 'Status code');
                })
            });
        }

        function setupPurchaseResultMessages() {
            $('div.purchase-result').on('click', function() {
                $(this).removeClass('message-showing');
            });
        }


        setupSwitchTables();
        setupBuyResources();
        setupTechUpgrades();
        setupPurchaseResultMessages();

    });
}(jQuery));

