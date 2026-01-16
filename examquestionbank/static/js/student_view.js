function ExamQuestionBankBlock(runtime, element) {
    var $element = $(element);
    
    // Scroll to top if flag is set from previous submission
    if (sessionStorage.getItem('scrollToTop') === 'true') {
        sessionStorage.removeItem('scrollToTop');
        setTimeout(function() {
            var examInfoPanel = $element.find('.exam-info-panel')[0];
            if (examInfoPanel) {
                examInfoPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }, 100);
    }
    
    var examSubmitBtn = $element.find('.submit-exam-btn')[0];

    let gettext;
    if ("ExamquestionbankI18n" in window || "gettext" in window) {
      gettext = window.ExamquestionbankI18n?.gettext || window.gettext;
    }

    if (typeof gettext == "undefined") {
      // No translations -- used by test environment
      gettext = (string) => string;
    }

    // Only set up submit button logic if it exists
    if (examSubmitBtn) {
        // Function to check if all problem submit buttons are enabled
        function checkAllProblemsReady() {
            var allReady = true;
            var submitButtons = $element.find('.vert-mod button.submit');

            // If no submit buttons found, disable exam button
            if (submitButtons.length === 0) {
                examSubmitBtn.disabled = true;
                return;
            }

            // Check if all submit buttons are enabled
            submitButtons.each(function() {
                if (this.disabled) {
                    allReady = false;
                }
            });

            examSubmitBtn.disabled = !allReady;
        }

        // Check on page load
        checkAllProblemsReady();

        // Listen for changes in all input elements within problems
        var vertMod = $element.find('.vert-mod');
        if (vertMod.length) {
            vertMod.on('input change', checkAllProblemsReady);
        }

        // Also observe changes to the disabled attribute of submit buttons
        var observer = new MutationObserver(checkAllProblemsReady);
        $element.find('.vert-mod button.submit').each(function() {
            observer.observe(this, { attributes: true, attributeFilter: ['disabled'] });
        });

        // Handler for Submit Exam
        $element.find('.submit-exam-btn').click(function() {
            // First click all problem submit buttons
            var submitButtons = $element.find('.vert-mod button.submit');
            submitButtons.each(function() {
                if (!this.disabled) {
                    this.click();
                }
            });

            // Wait for problem submissions to complete, then finalize exam submission
            setTimeout(function() {
                var handlerUrl = runtime.handlerUrl(element, 'submit_exam');
                $.ajax({
                    type: 'POST',
                    url: handlerUrl,
                    data: JSON.stringify({}),
                    success: function(result) {
                        if (!result.success) {
                            alert(result.error);
                            return;
                        }
                        // Reload to show updated grade and status
                        sessionStorage.setItem('scrollToTop', 'true');
                        window.location.reload();
                    },
                    error: function() {
                        alert(gettext('Error submitting exam. Please try again.'));
                    }
                });
            }, 2000);
        });
    }

    // Retry exam button handler - show confirmation modal
    $element.find('.retry-exam-btn').click(function() {
        var $modal = $('#retry-exam-modal');
        var $modalContent = $modal.find('.retry-modal-content');
        var position = $(this).data('modal-position') || 'top';
        
        // Remove any previous position classes
        $modalContent.removeClass('modal-position-top modal-position-bottom');
        
        // Add the appropriate position class
        $modalContent.addClass('modal-position-' + position);
        
        $modal.fadeIn(200);
    });

    // Modal close handlers
    $element.find('.retry-modal-close, .retry-modal-cancel').click(function() {
        $('#retry-exam-modal').fadeOut(200);
    });

    // Close modal when clicking overlay
    $element.find('.retry-modal-overlay').click(function() {
        $('#retry-exam-modal').fadeOut(200);
    });

    // Confirm retry handler
    $element.find('.retry-modal-confirm-btn').click(function() {
        var handlerUrl = runtime.handlerUrl(element, 'retry_exam');

        $.ajax({
            type: 'POST',
            url: handlerUrl,
            data: JSON.stringify({}),
            success: function(result) {
                sessionStorage.setItem('scrollToTop', 'true');
                window.location.reload();
            },
            error: function() {
                alert(gettext('Error retrying the exam. Please try again.'));
                $('#retry-exam-modal').fadeOut(200);
            }
        });
    });
}
