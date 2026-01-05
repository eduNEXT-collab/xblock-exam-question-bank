/* Javascript for ExamQuestionBankXBlock Student View. */

(function() {
  var examSubmitBtn = document.querySelector('.exam-submit-btn');
  if (!examSubmitBtn) return;

  // Function to check if all problem submit buttons are enabled
  function checkAllProblemsReady() {
    var allReady = true;
    var submitButtons = document.querySelectorAll('.vert-mod button.submit');
    
    // If no submit buttons found, disable exam button
    if (submitButtons.length === 0) {
      examSubmitBtn.disabled = true;
      return;
    }
    
    // Check if all submit buttons are enabled
    submitButtons.forEach(function(btn) {
      if (btn.disabled) {
        allReady = false;
      }
    });
    
    examSubmitBtn.disabled = !allReady;
  }
  
  // Check on page load
  checkAllProblemsReady();
  
  // Listen for changes in all input elements within problems
  // This will trigger when students answer questions
  var vertMod = document.querySelector('.vert-mod');
  if (vertMod) {
    vertMod.addEventListener('input', checkAllProblemsReady);
    vertMod.addEventListener('change', checkAllProblemsReady);
  }
  
  // Also observe changes to the disabled attribute of submit buttons
  // This catches cases where the problem logic enables/disables the button
  var observer = new MutationObserver(checkAllProblemsReady);
  document.querySelectorAll('.vert-mod button.submit').forEach(function(btn) {
    observer.observe(btn, { attributes: true, attributeFilter: ['disabled'] });
  });
  
  // Submit handler
  examSubmitBtn.addEventListener('click', function() {
    var submitButtons = document.querySelectorAll('.vert-mod button.submit');
    
    submitButtons.forEach(function(btn) {
      if (!btn.disabled) {
        btn.click();
      }
    });
  });
})();
