/* JavaScript for ExamQuestionBankXBlock Author View */
function ExamQuestionBankAuthorView(runtime, element, context) {
    'use strict';
    var $element = $(element);

    var refreshButton = $element.find('.btn-refresh-collections');
    var refreshCollectionsUrl = runtime.handlerUrl(element, 'refresh_collections');
	var updateMaxCountPerCollectionUrl = runtime.handlerUrl(element, 'update_max_count_per_collection');

    refreshButton.on('click', function (event) {
        event.preventDefault();
        refreshButton.prop('disabled', true);

        runtime.notify('save', { state: 'start', message: gettext('Refreshing collections...') });

		var usageId = $element.data("usageId");

        $.ajax({
            type: 'POST',
            url: refreshCollectionsUrl,
            data: JSON.stringify({}),
            contentType: 'application/json',
            dataType: 'json',
        })
            .done(function (response) {
                // Tell the parent window that XBlock data was saved
                window.parent.postMessage(
                    {
                        type: 'saveEditedXBlockData',
                        payload: { locator: usageId },
                    },
                    '*',
                );
                var message = $('<p>').text(gettext('Collections refreshed!'));
                $element.find('.bank-collections-section').append(message);
            })
            .fail(function () {
                runtime.notify('error', {
                    title: gettext('Failed to refresh collections'),
                    message: gettext('An error occurred while refreshing collections'),
                });
                var message = $('<p>').text(gettext('Failed to refresh collections'));
                $element.find('.bank-collections-section').append(message);
            })
            .always(function () {
                refreshButton.prop('disabled', false);
            });
    });

	var selectionDebounce;

	$element.find('.selected-quantity input[type="number"]').on('input change', function () {

		var value = $(this).val();

        // Allow empty (means: fallback to max_count)
        if (value !== '') {
            var parsed = parseInt(value, 10);

            if (!isNaN(parsed) && parsed < 1) {
                $(this).val(1);
            }
        }

		updateTotalSelected($element);
		clearTimeout(selectionDebounce);

		selectionDebounce = setTimeout(function () {

			var selectionData = {};

			$element.find('.selected-quantity input[type="number"]').each(function () {
				var key = $(this).attr('name');
				var raw = $(this).val();

				if (raw !== '') {
					var parsed = parseInt(raw, 10);
					if (!isNaN(parsed)) {
						selectionData[key] = parsed;
					}
				}
			});

			$.ajax({
				type: 'POST',
				url: updateMaxCountPerCollectionUrl,
				data: JSON.stringify(selectionData),
				contentType: 'application/json',
				dataType: 'json'
			})
			.fail(function () {
				runtime.notify('error', {
					title: gettext('Selection update failed'),
					message: gettext('Could not save selection.')
				});
			});

		}, 1000);

	});

    /**
     * Update total selected count
     */
    function updateTotalSelected($element) {
        var total = 0;
        var hasAnyValue = false;

        $element.find('.collection').each(function () {
            var rawValue = $(this).find('.selected-quantity input[type="number"]').val();
            if (rawValue !== '' && rawValue !== null) {
                var parsed = parseInt(rawValue, 10);

                if (!isNaN(parsed)) {
                    total += parsed;
                    hasAnyValue = true;
                }
            }
        });

        if (!hasAnyValue) {
            // All values are empty/null → fallback to max_count
            $element.find('.total-selected-count').text(context.max_count);
        } else {
            $element.find('.total-selected-count').text(total);
        }
    }

    updateTotalSelected($element);

    /**
     * Progressive View + Search
     */
    $element.find('.collection').each(function () {
        var $collection = $(this);
        var $allItems = $collection.find('.problem-item');
        var $buttonMore = $collection.find('.view-elements.more');
        var $buttonLess = $collection.find('.view-elements.less');
        var $search = $collection.find('.problem-search');
        var $resultsInfo = $collection.find('.search-results-info');
        var $clearButton = $collection.find('.search-clear-btn');

        $clearButton.hide();

        $clearButton.on('click', function () {
            $search.val('');
            $clearButton.hide();
            $activeItems = $allItems;
            resetPagination();
        });

        /* ---------- CONFIG ---------- */

        var INITIAL_VISIBLE = 6;
        var CHUNK_SIZE = 20;

        var $activeItems = $allItems;
        var visibleCount = INITIAL_VISIBLE;
        var debounceTimer;

		/* ---------- CONDITIONAL SEARCH VISIBILITY ---------- */
		if ($allItems.length <= INITIAL_VISIBLE) {
			$search.hide();
			$resultsInfo.hide();
		} else {
			$search.show();
		}

        /* ---------- INITIAL RENDER ---------- */
        resetPagination();

        /* ---------- VIEW MORE ---------- */
        $buttonMore.on('click', function () {
            var totalActive = $activeItems.length;
            var nextCount = Math.min(visibleCount + CHUNK_SIZE, totalActive);

            $activeItems.slice(visibleCount, nextCount).slideDown(150);
            visibleCount = nextCount;

            updateButtons();
        });

        /* ---------- VIEW LESS ---------- */
        $buttonLess.on('click', function () {
            $activeItems.slice(INITIAL_VISIBLE).slideUp(150);
            visibleCount = INITIAL_VISIBLE;
            updateButtons();

            // Smooth scroll to collection top for better UX
            $('html, body').animate(
                {
                    scrollTop: $collection.offset().top - 80,
                },
                200,
            );
        });

        /* ---------- SEARCH ---------- */
        $search.on('input', function () {
            clearTimeout(debounceTimer);

            var queryRaw = $search.val();
            var query = queryRaw.toLowerCase().trim();

            $clearButton.toggle(query.length > 0);

            debounceTimer = setTimeout(function () {
                if (query === '') {
                    $activeItems = $allItems;
                    resetPagination();
                    return;
                }

                $activeItems = $allItems.filter(function () {
                    return $(this).text().toLowerCase().includes(query);
                });

                $allItems.hide();

                if ($activeItems.length === 0) {
                    showNoResults();
                    $buttonMore.hide();
                    $buttonLess.hide();
                    updateResultsInfo();
                    return;
                }

                removeNoResults();
                resetPagination();
            }, 250); // Slightly smoother debounce
        });

        /* ---------- HELPERS ---------- */

        function updateResultsInfo() {
            var totalActive = $activeItems.length;

            if ($search.val().trim() === '') {
                $resultsInfo.text('');
                return;
            }

            if (visibleCount < totalActive) {
                $resultsInfo.text(`Showing ${visibleCount} of ${totalActive} results`);
            } else {
                $resultsInfo.text(`Showing all results`);
            }
        }

        function resetPagination() {
            removeNoResults();

            $allItems.hide();
            visibleCount = INITIAL_VISIBLE;

            $activeItems.slice(0, INITIAL_VISIBLE).show();

            updateButtons();
            updateResultsInfo();
        }

        function updateButtons() {
            var totalActive = $activeItems.length;

            if (totalActive <= INITIAL_VISIBLE) {
                $buttonMore.hide();
                $buttonLess.hide();
                updateResultsInfo();
                return;
            }

            if (visibleCount < totalActive) {
                $buttonMore.text(`View more (${totalActive - visibleCount})`).show();
                $buttonLess.hide();
            } else {
                $buttonMore.hide();
                $buttonLess.text('View less').show();
            }

            updateResultsInfo();
        }

        function showNoResults() {
            if (!$collection.find('.no-results').length) {
                $('<div class="no-results">No matching problems found. Try a different keyword.</div>').appendTo($collection);
            }
        }

        function removeNoResults() {
            $collection.find('.no-results').remove();
        }
    });
}
