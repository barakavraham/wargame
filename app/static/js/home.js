;(function($){
    'use strict';

    $(function() {
        let $body = $('body'),
            $loginForm = $('#login-form'),
            $loginFormBackground = $loginForm.find('.modal-background'),
            $loginBtn = $('#login-btn'),
            $registrationForm = $('#registration-form'),
            $registrationFormBackground = $registrationForm.find('.modal-background'),
            $registrationBtn = $('#registration-btn');

        function setupFormModals() {
            $loginBtn.on('click', function(){
                $body.removeClass('modal-active');
                $registrationForm.removeClass('one').addClass('out');
                $loginForm.addClass('one').removeClass('out');
                $body.addClass('modal-active');
            });

            $registrationBtn.on('click', function(){
                $body.removeClass('modal-active');
                $loginForm.removeClass('one').addClass('out');
                $registrationForm.addClass('one').removeClass('out');
                $body.addClass('modal-active');
            });

            $loginFormBackground.on('click', function(e){
                if ($(e.target).hasClass('modal-background')) {
                    $loginForm.addClass('out');
                    $('body').removeClass('modal-active');
                }
            });

            $registrationFormBackground.on('click', function(e) {
                if ($(e.target).hasClass('modal-background')) {
                    $registrationForm.addClass('out');
                    $('body').removeClass('modal-active');
                }
            });
        }

        setupFormModals();
    });
}(jQuery));

