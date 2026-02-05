/* JavaScript for ExamQuestionBankXBlock Author View */
function ExamQuestionBankAuthorView(runtime, element) {
    'use strict';

    var refreshButton = $(element).find('.btn-refresh-collections');
    var handlerUrl = runtime.handlerUrl(element, 'refresh_collections');

    refreshButton.on('click', function(event) {
        event.preventDefault();
        refreshButton.prop('disabled', true);

        $.ajax({
            type: 'POST',
            url: handlerUrl,
            data: JSON.stringify({}),
            contentType: 'application/json',
            dataType: 'json'
        }).done(function(response) {
            var message = $('<p>').text(response.message || 'Collections refreshed!');
            $(element).find('.bank-collections-section').append(message);
        }).fail(function() {
            var message = $('<p>').text('Failed to refresh collections');
            $(element).find('.bank-collections-section').append(message);
        }).always(function() {
            refreshButton.prop('disabled', false);
        });
    });
}
