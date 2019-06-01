;(function($){
    'use strict';

    $(function() {
        let $body = $('body'),
            $loginForm = $('#login-form'),
            $loginFormBackground = $loginForm.find('.popup-background'),
            $loginBtn = $('#login-btn'),
            $registrationForm = $('#registration-form'),
            $registrationFormBackground = $registrationForm.find('.popup-background'),
            $registrationBtn = $('#registration-btn');

        function collapseNav() {
            if ($('.navbar-collapse').hasClass('show')) {
                $('button.navbar-toggler').trigger('click');
            }
        }

        function resetForm($form) {
            $form.find('input').not(':checkbox, :radio').val('').addClass('mb-4');
            $form.find('.invalid-feedback').remove();
            $form.find('.is-invalid').removeClass('is-invalid');
        }

        function setupFormInputs() {
            $('form input').not(':checkbox, radio').on('input', function() {
                $(this).removeClass('is-invalid').addClass('mb-4');
                $(this).parent('div').find('.invalid-feedback').remove();
            });
        }

        function setupFormPopups() {
            $loginBtn.on('click', function(){
                collapseNav();
                $body.removeClass('popup-active');
                $registrationForm.removeClass('one').addClass('out');
                $loginForm.addClass('one').removeClass('out');
                $body.addClass('popup-active');
            });

            $registrationBtn.on('click', function(){
                collapseNav();
                $body.removeClass('popup-active');
                $loginForm.removeClass('one').addClass('out');
                $registrationForm.addClass('one').removeClass('out');
                $body.addClass('popup-active');
            });

            $loginFormBackground.on('click', function(e){
                if ($(e.target).hasClass('popup-background')) {
                    $loginForm.addClass('out');
                    $('body').removeClass('popup-active');
                    resetForm($loginForm);
                }
            });

            $registrationFormBackground.on('click', function(e) {
                if ($(e.target).hasClass('popup-background')) {
                    $registrationForm.addClass('out');
                    $('body').removeClass('popup-active');
                    resetForm($registrationForm);
                }
            });
        }

        function openInvalidFormIfNeeded() {
            if (window.jsVars.invalidFormButton) {
                $(`#${window.jsVars.invalidFormButton}`).trigger('click');
                setTimeout(function() {
                    $('[id*="__lpform"]').remove();
                }, 1000);
            }
        }

        setupFormPopups();
        setupFormInputs();
        // This function needs to be last
        openInvalidFormIfNeeded();
    });
}(jQuery));

