/* this app handel's common facilites */
$(function () {
    // article tag click event
    let searchModal = $("#search-modal");
    $(".article-tag").on('click', TagClick);

    function TagClick(e){
        e.preventDefault();
        searchModal['foundation']('open');
        // replace keyword field value with tag name
        let tag_name = $(this).html();
        searchModal.find('.input-group-field').val(`TAG:${tag_name}`);
        // submit form
        searchModal.find('form').submit();
    }
});