function ExamQuestionBankBlock(runtime, element) {
    var $element = $(element);
    var examSubmitBtn = $element.find('.submit-exam-btn')[0];

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
                        window.location.reload();
                    },
                    error: function() {
                        alert('Error submitting exam. Please try again.');
                    }
                });
            }, 2000);
        });
    }

    $element.find('.retry-exam-btn').click(function() {

        var handlerUrl = runtime.handlerUrl(element, 'retry_exam');

        $.ajax({
            type: 'POST',
            url: handlerUrl,
            data: JSON.stringify({}),
            success: function(result) {
                window.location.reload();
            },
            error: function() {
                alert('Error retrying the exam. Please try again.');
            }
        });
    });
}
