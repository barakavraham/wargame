$('.attack-button').on('click', function() {
    $(this).closest('div.table-parent').find('.defense').hide();
    $(this).closest('div.table-parent').find('.attack').show();
});

$('.defense-button').on('click', function() {
    $(this).closest('div.table-parent').find('.attack').hide();
    $(this).closest('div.table-parent').find('.defense').show();
});