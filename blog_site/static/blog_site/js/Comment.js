$(function(){
    let form = $("#comment-form");
    let comment_container = $("#comment_container");
    let modal = $("#Modal");
    let comment_count = document.querySelector('#comment_counter').dataset['count'];
    comment_count = parseInt(comment_count);
    console.log(comment_count);

    form.on('submit', function(){
        $.ajax({
            "url":$(this).attr('action'),
            "type": $(this).attr('method'),
            "dataType": "json",
            "data":$(this).serialize(),
            'success':function(data){
                // noinspection JSUnresolvedVariable
                if (data.successful === true){
                    // noinspection JSUnresolvedVariable
                    $(".comment-form-input").val("");
                    comment_container.append(data.html_content);
                    AttachEvents();
                    comment_count++;
                    updateCommentCount();
                }
            }
        });
        return false;
    });
    function submitUpdateComment(event){
        let modal = $("#Modal");
        event.preventDefault();
        $.ajax({
            'url':$(this).attr('action'),
            'type':'post',
            'dateType':'json',
            'data': $(this).serialize(),
            'success': function(data){
                modal.foundation('close');
                let form = $("#comment-update-form");
                let id = form.attr('data-comment');
                let comment_container = $("#comment_" + id);
                if (data.successful === true){
                comment_container.replaceWith(data.html_content);
                AttachEvents();
                } else{
                    modal.html(data.html_form)
                }
            },
        });
        return false;
    }
    function UpdateComment(event){
       event.preventDefault();
        $.ajax({
           'url':$(this).attr('href'),
           'type': 'get',
           'dataType': 'json',
           'beforeSend': function(){
               modal.foundation('open');
           },
           'success': function(data){
              if (data.successful === true){
                  modal.html(data.html_form);
              }
           },
       });
    }
    function DeleteComment(event){
       let id = $(this).attr('data-comment');
       event.preventDefault();

        $.ajax({
           'url':$(this).attr('href'),
           'type': 'get',
           'dataType': 'json',
            'success': function(){
               let comment = $("#comment_" + id);
               comment.html('');
               comment.remove();
                comment_count--;
                updateCommentCount();
            }
       });
    }
    function createReply(){
        let reply_container_id = $(this).attr('data-comment');
        $.ajax({
            'url':$(this).attr('action'),
            'data':$(this).serialize(),
            'type':$(this).attr('method'),
            'dataType':'json',
            'success': function(data){
                if (data.successful === true){
                    let reply_container = $(".reply-container_" + reply_container_id);
                    reply_container.append(data.html_content);
                    modal.foundation('close');
                    // reattach listeners for all replies
                    AttachEvents();
                } else{
                    modal.html(data.html_form)
                }
            }
        });
        return false;
    }
    function toggleCreate(event){
        event.preventDefault();

        $.ajax({
            'url':$(this).attr('href'),
            'type': 'get',
            'dataType':'json',
            'beforeSend': function(){
                modal.foundation('open');
            },
            'success': function(data){
                if(data.successful === true){
                    modal.html(data.html_form)
                }
            },
        });
        return false;
    }
    function deleteReply(){
        let id = $(this).attr('data-reply');
        event.preventDefault();
        $.ajax({
           'url':$(this).attr('href'),
           'type': 'get',
           'dataType': 'json',
            'success': function(){
               let reply = $("#reply_" + id);
               reply.remove();
            }
       });
    }
    function updateReply(){
        let reply_id = $(this).attr('data-reply');
        $.ajax({
            'url':$(this).attr('action'),
            'data':$(this).serialize(),
            'type':$(this).attr('method'),
            'dataType':'json',
            'success': function(data){
                if (data.successful === true){
                    let reply = $("#reply_" + reply_id);
                    reply.replaceWith(data.html_content);
                    modal.foundation('close');
                    // reattach listeners for all replies
                    AttachEvents()
                } else{
                    modal.html(data.html_form)
                }
            }
        });
        return false;
    }
    function toggleUpdate(event){
            event.preventDefault();
            $.ajax({
                'url':$(this).attr('href'),
                'type': 'get',
                'dataType':'json',
                'beforeSend': function(){
                    modal.foundation('open');
                },
                'success': function(data){
                    if(data.successful === true){
                        modal.html(data.html_form)
                    }
                },
            });
            return false;
        }

    function updateCommentCount(){
        let comment_counter = document.querySelector('#comment_counter');
        if (comment_count < 0){comment_count = 0;}
        comment_counter.innerHTML = `Comments ${comment_count}`;
    }

    function AttachEvents(){
            let delete_comment_button = $(".js-delete-comment");
            delete_comment_button.on('click', DeleteComment);
            let update_comment_button = $(".js-update-comment");
            update_comment_button.on('click', UpdateComment);
            let modal = $("#Modal");
            modal.on('submit', '#comment-update-form', submitUpdateComment);

            // reply_create
            let reply_button = $('.js-reply_to_comment');
            reply_button.on('click', toggleCreate);
            modal.on('submit', '#reply-create-form', createReply);

            // reply_update
           let reply_update_button = $(".js-update-reply");
           reply_update_button.on('click', toggleUpdate);
           modal.on('submit', '#reply-update-form', updateReply);

            //reply delete
            let delete_reply_button = $(".js-delete-reply");
            delete_reply_button.on('click', deleteReply);
    }
    AttachEvents();
});

