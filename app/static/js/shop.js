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
            $prices.empty()
            if (prices) {
                for (let resource in prices) {
                    $prices.append('<div class="col text-center mt-2"></div>');
                    let $resourceCol = $prices.find('.col').last();
                    $resourceCol.append(`<p class="card-text mb-0"><img class="resource-img img-fluid"  src="${prices[resource]['picture']}" /></p>`);
                    $resourceCol.append(`<p class="card-text">${prices[resource].price}</p>`);
                    $btn.data('cost-'+resource, prices[resource].price);
                }
            } else {
                $prices.append('<p class="col text-center">Maxed out</p>')
                $btn.remove();
            }
        }

        function purchaseOpenMessage($divMessage, purchaseSuccess, text) {
            $('div.purchase-result').text('');
            $divMessage.removeClass('success, fail');
            $divMessage.text('');
            if (purchaseSuccess)
                $divMessage.addClass('success').text(text);
            else
                $divMessage.addClass('fail').text(text);
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
                    $purchaseResult.addClass('fail').text('Please enter a valid amount');
                    return false;
                }

                if (!canBuy($buyBtn, amount)) {
                    purchaseSuccess = false;
                    return false
                }
                   
                else 
                    purchaseSuccess = true;
                

                $.gameApiPost('shop/buy_resources', {
                    item: $buyBtn.data('item'),
                    amount: amount
                }).done(function() {
                    purchaseOpenMessage($purchaseResult, purchaseSuccess, 'Purchase success')
                    $buyBtn.closest('.weapon-container').find('.current-weapon-amount').text(currentResourceAmount + amount);
                    setUserResources($buyBtn);
                    $purchaseResult.addClass('success').text('Purchase successful');
                    $amountInput.val('');
                }).fail(function({ status }) {
                    if (status === 400)
                        purchaseOpenMessage($purchaseResult, purchaseSuccess, 'Not enough resources');
                    else
                        purchaseOpenMessage($purchaseResult, purchaseSuccess, 'Status code');
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
                }
                
                else 
                     purchaseSuccess = true;
                

                $.gameApiPost('shop/upgrade', {
                    upgrade: $upgradeBtn.data('item-upgrade'),
                    level: nextUpgradeLevel
                }).done(function(data) {
                    purchaseOpenMessage($purchaseResult, purchaseSuccess, 'Purchase success')
                    setUserResources($upgradeBtn);
                    if (nextUpgradeLevel < 5)
                        $upgradeBtn.closest('.upgrade-container').find('.current-upgrade-level').text(nextUpgradeLevel);
                    $upgradeBtn.data('next-level', nextUpgradeLevel + 1);
                    if (data.picture)
                        $upgradeBtn.closest('.upgrade-container').find('.card-img-top').attr('src', data.picture);

                    setButtonPrices($upgradeBtn, data.prices);

                    $purchaseResult.addClass('success').text('Purchase successful');
                }).fail(function({ status, max_level }) {
                    if (status === 400)
                        purchaseOpenMessage($purchaseResult, purchaseSuccess, 'Not enough resources')
                    else if (max_level)
                        $purchaseResult.addClass('fail').text('200');
                    else
                        purchaseOpenMessage($purchaseResult, purchaseSuccess, 'Status code');
                })
            });
        }


        setupSwitchTables();
        setupBuyResources();
        setupTechUpgrades();

    });
}(jQuery));

