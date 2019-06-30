;(function($){
    'use strict';

    $(function() {
        let $body = $('body'),
            $showProfileBtn = $('.show-profile'),
            $profileBackground = $('.profile-background'),
            $armyProfile = $('#army-profile'),
            $armyProfilePopup = $armyProfile.find('.popup');

        function setupOpenProfileWindow(){
            $showProfileBtn.on('click', function(){
                $armyProfilePopup.empty();
                let $button = $(this),
                    army_email = $button.data('army-email'),
                    army_rank = $button.data('army-rank');
                $.gameApiGet(`attack/user_profile/${army_email}`
                ).done(function(html_profile){
                    $armyProfilePopup.append(html_profile);
                    $armyProfilePopup.find('#rank').text(`rank: ${army_rank}`);
                    $armyProfile.removeAttr('class').addClass($button.attr('id'));
                    $body.addClass('popup-active');
                    setupAttackButton();
                });
            })
        }

        function setupCloseProfileWindow() {
            $profileBackground.on('click', function(e){
                if ($(e.target).hasClass('profile-background')) {
                    $(this).closest('#army-profile').addClass('out');
                    $body.removeClass('popup-active');
                }
            })
        }

        function setupAttackButton() {
            $('#attack-btn').on('click', function(){
                // let $attack = $armyProfile.find('.attack');
                // $attack.empty();
                // $attack.removeClass('justify-content-around');
                // $attack.addClass('justify-content-evenly');
                // $attack.append("<button class='align-items-center mt-3' id='attack-btn-1'> Attack 1 </button>");
                // $attack.append("<button class='align-items-center mt-3' id='attack-btn-2'> Attack 2 </button>");
                $.gameApiPost('attack/attack', {
                    attacker_user_id: 1,
                    attacked_user_id: 2
                }).done(({ attacker_results, attacked_results, is_winner }) => {
                    console.log(attacker_results);
                    console.log(attacked_results);
                    console.log(is_winner);
                });
            })
        }

        setupOpenProfileWindow();
        setupCloseProfileWindow();
    });
}(jQuery));
