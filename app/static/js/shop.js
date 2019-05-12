$(document).ready(function(){

    function shopApiPost(url, data) {
        return $.ajax({
            url: '/api/shop' + url,
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json'
        });
    }

    $('.amount').on('input', function() {
        $(this).val($(this).val().replace(/\D/g, ''));
    });

    $('.buy-btn').on('click', function() {
        let $userRsources = $('#user-resources'),
            $buyBtn = $(this),
            $purchaseResult = $buyBtn.next('div.purchase-result'),
            $amountInput = $buyBtn.prev('.amount'),
            amount = Number($amountInput.val()),
            currentGold = $userRsources.data('army-gold'),
            currentMetal = $userRsources.data('army-metal'),
            currentResourceAmount = Number($buyBtn.closest('tr').find('.current-amount').text()),
            goldCost = $buyBtn.data('cost-gold'),
            metalCost = $buyBtn.data('cost-metal');

        $('div.purchase-result').text('');
        $purchaseResult.removeClass('success, fail');
        $purchaseResult.text('');

        if (amount <= 0) {
            $amountInput.val('');
            $purchaseResult.addClass('fail').text('Please enter a valid amount');
            return false;
        }

        if (goldCost * amount > currentGold || metalCost * amount > currentMetal) {
            $purchaseResult.addClass('fail').text('Not enough resources');
            return false;
        }


        shopApiPost('/buy_resources', {
            item: $buyBtn.data('item'),
            amount: amount
        }).done(function() {
            $buyBtn.closest('tr').find('.current-amount').text(currentResourceAmount + amount);
            $('#current-gold-amount').text(currentGold - goldCost * amount);
            $('#current-metal-amount').text(currentMetal - metalCost * amount);
            $('#user-resources').data('army-gold', currentGold - goldCost * amount);
            $('#user-resources').data('army-metal', currentMetal - metalCost * amount);
            $purchaseResult.addClass('success').text('Purchase successful');
            $amountInput.val('');
        }).fail(function() {
            $purchaseResult.addClass('fail').text('Not enough resources');
        });

    });

});
