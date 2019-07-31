;(function($){
    'use strict';

    $(function() { 
        let $body = $('body'),
            $sendMailResult = $('.send-mail-result'),
            $openMailForm = $('.show-new-mail'),
            $mailBackground = $('.new-mail-background'),
            $readMailBackground = $('.read-mail-background'),
            $mailsButton = $('#mail-btn'),
            $defendButton = $('#defend-btn'),
            armies = [];
            console.log($sendMailResult.outerWidth());
            
        function setupButtons() {
            $mailsButton.on('click', function(){
                $('.defend-table').hide();
                $('.receive-mails-table').show();
            })
            
            $defendButton.on('click', function(){
                $('.receive-mails-table').hide();
                $('.defend-table').show();
            })
        }

        function setupSendMailResult($sendResultDiv, sendSuccess, text) {
            $sendResultDiv.removeClass('message-showing').empty();
            $sendResultDiv.append(`<p>${text}</p>`).addClass('message-showing');
            if (sendSuccess)
                $sendResultDiv.find('p').addClass('bg-success');
            else
                $sendResultDiv.find('p').addClass('bg-warning');
            setTimeout(function() {
                $sendResultDiv.removeClass('message-showing');
            }, 2000)
        }

        function LiveSearch() {
            $('.mail-recipient-army').keyup(function(){
                $('.users-list').empty();
                let $liveSearchInput = $('.mail-recipient-army').val();
                if ($liveSearchInput.length >= 3) {
                    $.gameApiGet(`mail/get_armies/${$liveSearchInput}`
                    ).done(function(armies) {
                        if (armies.length > 0) {
                            for (let army of armies) {
                                $('.users-list').append(`<div class="list-group-users text-left ml-2"> <img class="army-avatar" src="${army.picture_url}"/>  ${army.name}</div>`);
                                $('.list-group-users').last().on('click', function() {
                                    $('.mail-recipient-army').val(army.name);
                                    $('.users-list').hide();
                                });
                            }
                            $('.users-list').show();
                        }
                    });
                }
                else {
                    $('.users-list').hide();
                }
            });
        }

        function setupReadMailWindow() {
            $('.read-mail').on('click', function(){
                let $author = $(this),
                    $mailTitle = $author.data('mail-title'),
                    $mailContent = $author.data('mail-content'),
                    $readMailWindow = $('#read-mail-window');

                $('.read-mail-title').text($mailTitle);
                $('.read-mail-content').text($mailContent);
                $readMailWindow.removeAttr('class').addClass('five');
                $body.addClass('popup-active');  
                setupCloseMailWindow();      
            })
        }

        function setupOpenMailWindow() {
            $openMailForm.on('click', function() {
                let $newMail = $('#new-mail');

                $newMail.removeAttr('class').addClass('five');
                $body.addClass('popup-active');
            });
        }

        function CloseMailWindow() {
            $body.removeClass('popup-active');
            $('#new-mail').addClass('out');
            $('.mail-recipient-army').val("");
            $('.mail-title').val("");
            $('.mail-content').val("");
            $('#read-mail-window').addClass('out');
            $('.read-mail-title').text('');
            $('.read-mail-content').text('');
            $('.users-list').empty();
            $('.users-list').hide();
            armies = [];
        }

        function setupCloseMailWindow() {
            $mailBackground.on('click', function(e) {
                if ($(e.target).hasClass('new-mail-background')) {
                    CloseMailWindow();
                }
            });

            $readMailBackground.on('click', function(e) {
                if ($(e.target).hasClass('read-mail-background')) {
                    CloseMailWindow();
                }
            });
        }

        function vaildate_letters($title, $content) {
            if ($title.length < 2 || $content.length <2)
                return false
            return true
        }

        function SendMail() {
            $('.btn').on('click', function() {
                let $currentUserName = $(this).data('current-user-name'),
                    $mailRecipient = $('.mail-recipient-army').val(),
                    $mailTitle = $('.mail-title').val(),
                    $mailContent = $('.mail-content').val();
                
                if ($currentUserName === $mailRecipient) {
                    setupSendMailResult($sendMailResult, false, 'You cant send mail to yourself');
                    return false
                }

                if (vaildate_letters === false){
                    setupSendMailResult($sendMailResult, false, 'Title/Content must be more than 1 letter');
                    return false
                }

                $.gameApiPost('mail/send_mail', {
                    recipient_army: $mailRecipient,
                    title: $mailTitle,
                    content: $mailContent
                }).done(function(data) {
                    setupSendMailResult($sendMailResult, true, data.send_result);
                    setTimeout(function(){CloseMailWindow()}, 1000);
                }).fail(function(data) {
                    setupSendMailResult($sendMailResult, false, data.responseJSON.send_result);
                });
            })
        }
        setupReadMailWindow();
        setupButtons();
        LiveSearch();
        SendMail();
        setupOpenMailWindow();
        setupCloseMailWindow();
    });
}(jQuery));
