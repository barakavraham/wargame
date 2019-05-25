$(document).ready(function() {

    let $techBtn = $('.tech-btn')

    function shopApiPost(url, data) {
        return $.ajax({
            url: '/api/shop' + url,
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json'
        });
    }

    $('.tech-btn').on('click', function() {
        $('.table-container').find('table').hide()
        $('.table-container').find('table').next('table').show()
    });

    $('.weapon-btn').on('click', function() {
        $('.table-container').find('table').next('table').hide()
        $('.table-container').find('table').first().show()
    });

    $('.amount').on('input', function() {
        $(this).val($(this).val().replace(/\D/g, ''));
    });

    $('.buy-btn').on('click', function() {
        let $userResources = $('#user-resources'),
            $buyBtn = $(this),
            $purchaseResult = $buyBtn.next('div.purchase-result'),
            $amountInput = $buyBtn.prev('.amount'),
            amount = Number($amountInput.val()),
            currentCoin = $userResources.data('army-coin'),
            currentMetal = $userResources.data('army-metal'),
            currentResourceAmount = Number($buyBtn.closest('tr').find('.current-amount').text()),
            coinCost = $buyBtn.data('cost-coin'),
            metalCost = $buyBtn.data('cost-metal');

        $('div.purchase-result').text('');
        $purchaseResult.removeClass('success, fail');
        $purchaseResult.text('');

        if (amount <= 0) {
            $amountInput.val('');
            $purchaseResult.addClass('fail').text('Please enter a valid amount');
            return false;
        }

        if (coinCost * amount > currentCoin || metalCost * amount > currentMetal) {
            $purchaseResult.addClass('fail').text('Not enough resources');
            return false;
        }


        shopApiPost('/buy_resources', {
            item: $buyBtn.data('item'),
            amount: amount
        }).done(function() {
            $buyBtn.closest('tr').find('.current-amount').text(currentResourceAmount + amount);
            $('#current-coin-amount').text(currentCoin - coinCost * amount);
            $('#current-metal-amount').text(currentMetal - metalCost * amount);
            $('#user-resources').data('army-coin', currentCoin - coinCost * amount);
            $('#user-resources').data('army-metal', currentMetal - metalCost * amount);
            $purchaseResult.addClass('success').text('Purchase successful');
            $amountInput.val('');
        }).fail(function({ status }) {
            if (status === 400)
                $purchaseResult.addClass('fail').text('Not enough resources');
        })
    });

    $('.upgrade-btn').on('click', function() {
        let $userResources = $('#user-resources'),
            $upgradeBtn = $(this),
            $purchaseResult = $upgradeBtn.next('div.purchase-result'),
            currentCoin = $userResources.data('army-coin'),
            currentMetal = $userResources.data('army-metal'),
            currentWood = $userResources.data('army-wood'),
            nextUpgradeLevel = $upgradeBtn.data('next-level'),
            coinCost = $upgradeBtn.data('cost-upgrade-coin'),
            woodCost = $upgradeBtn.data('cost-upgrade-wood'),
            metalCost = $upgradeBtn.data('cost-upgrade-metal');

        $('div.purchase-result').text('');
        $purchaseResult.removeClass('success, fail');
        $purchaseResult.text('');
        if (coinCost > currentCoin || woodCost > currentWood || metalCost > currentMetal) {
            $purchaseResult.addClass('fail').text('Not enough resources');
            return false;
        }

        shopApiPost('/upgrade', {
            upgrade: $upgradeBtn.data('item-upgrade'),
            level: nextUpgradeLevel
        }).done(function(data) {
            $upgradeBtn.closest('tr').find('.current-level').text(nextUpgradeLevel);
            $('#current-coin-amount').text(currentCoin - coinCost);
            $('#current-metal-amount').text(currentMetal - metalCost);
            $('#current-wood-amount').text(currentWood - woodCost);
            $('#user-resources').data('army-coin', currentCoin - coinCost);
            $('#user-resources').data('army-metal', currentMetal - metalCost);
            $('#user-resources').data('army-wood', currentWood - woodCost);
            $upgradeBtn.data('next-level', nextUpgradeLevel + 1);

            if (data.prices) {
                $upgradeBtn.data('cost-upgrade-coin', data.prices.coin);
                $upgradeBtn.data('cost-upgrade-wood', data.prices.wood);
                $upgradeBtn.data('cost-upgrade-metal', data.prices.metal);
                $upgradeBtn.closest('tr').find('.coin-price').text(data.prices.coin);
                $upgradeBtn.closest('tr').find('.wood-price').text(data.prices.wood);
                $upgradeBtn.closest('tr').find('.metal-price').text(data.prices.metal);
            } else {
                $upgradeBtn.closest('tr').find('.coin-price').text('NaN');
                $upgradeBtn.closest('tr').find('.wood-price').text('NaN');
                $upgradeBtn.closest('tr').find('.metal-price').text('NaN');
            }

            $purchaseResult.addClass('success').text('Purchase successful');
        }).fail(function({ status, max_level }) {
            if (status === 400)
                $purchaseResult.addClass('fail').text('Not enough resources');
            else if (max_level)
                $purchaseResult.addClass('fail').text('200');
        })
    });
});

