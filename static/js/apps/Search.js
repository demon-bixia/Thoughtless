// we use one modal for all operations

$(function (e) {
    let modal = $("#search-modal");

    function SetupEvents() {
        //search event
        $('#search-form').on('submit', Search);

        // delete letter event
        $('#search-form .backspace-icon').on('click', Backspace);

        // toggle modal event
        $("#js-search-button").on('click', e => {
            e.preventDefault(); // cancel default event
        });

        // submit form event
        $("#js-submit-search-button").on('click', function () {
            $('#search-form').submit();
        });
    }

    function Backspace(e) {
        let backspace = $(this).find('i').hasClass('fa-backspace');
        let inputField = $(this).siblings('.input-group-field');
        let value = inputField.val();
        let length = value.length;

        // if backspace icon clicked
        if (backspace) {
            // if length is zero remove back space icon
            if (length) {
                let newValue = value.slice(0, length - 1); // remove a letter
                inputField.val(newValue);
            } else {
                //  remove icon when all text is deleted
                $(this).find('i').removeClass('fa fa-backspace');
            }
        }
    }

    /* when tag is clicked */
    function TagClick(e) {
        e.preventDefault();
        // replace keyword field value with tag name
        let tag_name = $(this).html();
        modal.find('.input-group-field').val(`TAG:${tag_name}`);
        // submit form
        modal.find('form').submit();
    }

    function Search(e) {
        e.preventDefault(); // stop form from submitting
        let data = $(this).serialize(); // change form data into json
        let url = $(this).attr('action');

        toggleSpinner();

        Request(url, data).then(
            // if request successful
            function (response) {
                // if operation successful
                if (response['success']) {
                    // add found articles to modal
                    $("#article-container .article-wrapper").html(response['html_content']);
                    toggleSpinner();
                    // attach tag clicked events for new element
                    $(".article-tag").on('click', TagClick);
                } else {
                    // show a no result found message when operation errors arise
                    let noResult = $(`<div class="no-result"><p>no result found</p></div>`);
                    $("#article-container .article-wrapper").html(noResult);
                    console.log(response['message']); // for debug purposes
                    toggleSpinner();
                }
            },
            function (error) {
                // log error for debug purposes
                console.error("request error in func: Search file: Search.js", error);
            }
        )
    }

    /* UTILS */

    /* changes spinner from active to inactive */
    function toggleSpinner(){
        $('#article-container .spinner-wrapper').toggleClass('active');
    }

    /* request template function used by requests in this module */
    function Request(url, data) {
        // return ajax promise
        return $.ajax({
            "url": url,
            "type": "get",
            "dataType": "json",
            "data": data,
        });
    }

    SetupEvents();
});
