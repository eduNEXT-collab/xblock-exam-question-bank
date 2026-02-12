/* JavaScript for ExamQuestionBankXBlock Author View */
function ExamQuestionBankAuthorView(runtime, element) {
    'use strict';

    var refreshButton = $(element).find('.btn-refresh-collections');
    var handlerUrl = runtime.handlerUrl(element, 'refresh_collections');

    refreshButton.on('click', function(event) {
        event.preventDefault();
        refreshButton.prop('disabled', true);
        
        runtime.notify('save', {state: 'start', message: gettext('Refreshing collections...')});

        $.ajax({
            type: 'POST',
            url: handlerUrl,
            data: JSON.stringify({}),
            contentType: 'application/json',
            dataType: 'json'
        }).done(function(response) {
            // Tell the parent window that XBlock data was saved
            window.parent.postMessage({
                type: 'saveEditedXBlockData',
                payload: {}
            }, '*');
            var message = $('<p>').text(gettext('Collections refreshed!'));
            $(element).find('.bank-collections-section').append(message);
        }).fail(function() {
            runtime.notify('error', {
                title: gettext('Failed to refresh collections'),
                message: gettext('An error occurred while refreshing collections')
            });
            var message = $('<p>').text(gettext('Failed to refresh collections'));
            $(element).find('.bank-collections-section').append(message);
        }).always(function() {
            refreshButton.prop('disabled', false);
        });
    });
}
