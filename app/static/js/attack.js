;(function($){
    'use strict';

    $(function() {

        function openProfileWindow(){
            $('.button').on('click', function(){
                $('#army-profile').remove();
                let $button = $(this),
                    army_email = $button.data('army-email'),
                    army_rank = $button.data('army-rank');
                $.gameApiGet(`attack/user_profile/${army_email}`
                ).done(function(html_profile){
                    $('body').append(html_profile);
                    $('#army-profile').find('#rank').text(`rank: ${army_rank}`);
                    $('#army-profile').removeAttr('class').addClass($button.attr('id'));
                    $('body').addClass('popup-active');
                    attack();
                    closeProfileWindow();
                })
            })
        }

        function closeProfileWindow() {
            $('.army-profile-background').on('click', function(e){
                if ($(e.target).hasClass('army-profile-background')) {
                    $(this).closest('#army-profile').addClass('out');
                    $('body').removeClass('popup-active');
                }
            })
        }

        function attack() {
            $('#attack-btn').on('click', function(e){
                let $attack = $('#army-profile').find('.attack');
                $attack.empty();
                $attack.removeClass('justify-content-around');
                $attack.addClass('justify-content-evenly');
                $attack.append("<button class='align-items-center mt-3' id='attack-btn-1'> Attack 1 </button>")
                $attack.append("<button class='align-items-center mt-3' id='attack-btn-2'> Attack 2 </button>")
            })
        }
    openProfileWindow();
    });
}(jQuery));
