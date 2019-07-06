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
                    user_id = $button.data('user-id'),
                    army_rank = $button.data('army-rank');
                $.gameApiGet(`attack/user_profile/${user_id}`
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
                $.gameApiPost('attack/attack', {
                    attacker_user_id: $(this).data('attacker-user-id'),
                    attacked_user_id: $(this).data('attacked-user-id'),
                    weapon_types: JSON.stringify([])
                }).done(({ is_winner, url }) => {
                    console.log(is_winner);
                    console.log(url);
                });
            })
        }

        setupOpenProfileWindow();
        setupCloseProfileWindow();
    });
}(jQuery));
