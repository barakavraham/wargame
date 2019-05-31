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

        function collapseNav() {
            if ($('.navbar-collapse').hasClass('show')) {
                $('button.navbar-toggler').trigger('click');
            }
        }

        function resetForm($form) {
            $form.find('input').not(':checkbox, :radio').val('');
            $form.find('.invalid-feedback').remove();
            $form.find('.is-invalid').removeClass('is-invalid');
        }

        function setupFormInputs() {
            $('form input[type="text"]').on('input', function() {
                $(this).removeClass('is-invalid');
                $(this).parent('div').find('.invalid-feedback').remove();
            });
        }

        function setupFormModals() {
            $loginBtn.on('click', function(){
                collapseNav();
                $body.removeClass('modal-active');
                $registrationForm.removeClass('one').addClass('out');
                $loginForm.addClass('one').removeClass('out');
                $body.addClass('modal-active');
            });

            $registrationBtn.on('click', function(){
                collapseNav();
                $body.removeClass('modal-active');
                $loginForm.removeClass('one').addClass('out');
                $registrationForm.addClass('one').removeClass('out');
                $body.addClass('modal-active');
            });

            $loginFormBackground.on('click', function(e){
                if ($(e.target).hasClass('modal-background')) {
                    $loginForm.addClass('out');
                    $('body').removeClass('modal-active');
                    resetForm($loginForm);
                }
            });

            $registrationFormBackground.on('click', function(e) {
                if ($(e.target).hasClass('modal-background')) {
                    $registrationForm.addClass('out');
                    $('body').removeClass('modal-active');
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

        setupFormModals();
        setupFormInputs();
        // This function needs to be last
        openInvalidFormIfNeeded();
    });
}(jQuery));

