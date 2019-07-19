function get_restaurant_timeline_list(){
    var restaurant_timeline_div = $('#restaurant_timeline');
    var api_url = '/api/timeline/restaurant/';
    
    $.ajax({
        type: 'GET',
        url: api_url,
        dataType: 'json',
        error: function (data) {
            if(data.status == 404){
                var timeline_div = data.responseJSON['error'];
                restaurant_timeline_div.append(timeline_div);
            }
        },
        success: function (data) {
            var restaurants = data;
            var index = 0;
            restaurants.forEach(function(restaurant) {
                var timeline_div='';
                var timeline_type=restaurant.timeline_type;
                var timeline_id = restaurant.restaurant_timeline_id;
                 timeline_div   =
                    `<li id="timeline_li`+index+`">
                        <div id="timeline_badge`+index+`" ></div>
                        <div class="timeline-panel">
                            <div class="timeline-heading">
                                <div class="row">
                                    <span class="badge badge-pill badge-primary mr-2" id="min_price`+index+`">
                                    최소금액:
                                    </span>
                                    <span class="badge badge-pill badge-info" id="delivery_charge`+index+`">
                                    배달요금:
                                    </span>
                                </div>
                                <div class="row align-items-center">
                                    <div class="m-3">
                                        <img id="restaurant_img`+index+`"
                                            alt="..." width=80px height=80px>
                                    </div>
                                    <h5 class="timeline-title" id="restaurant_title`+index+`"></h5>
                                </div>
                                <span><small class="text-muted"><i class="fa fa-time" id="create_time`+index+`"></i> </small>
                                </span>
                            </div>
                            <hr>
                            <span id="timeline_type`+index+`">
                            </span>
                            <div class="timeline-title" id="timeline_title`+index+`">
                            </div>
                            <div class="timeline-body" id="timeline_content`+index+`">
                            </div>
                            <hr>
                            <div class="row">
                                <div class="container" id="like_container`+index+`">
                                </div>
                            </div>
                        </div>
                    </li>`;

                if(timeline_type <= 2 | timeline_type==5){
                    restaurant_timeline_div.append(timeline_div);
                    if(timeline_type==1){//공지사항
                        $('#timeline_li'+index).attr('class', 'timeline-inverted');
                        $('#timeline_badge'+index).attr('class', 'timeline-badge success');
                        $('#timeline_badge'+index).append('<i class="fa fa-exclamation"></i>');
                        $('#timeline_type'+index).attr('class', 'badge badge-pill badge-success mb-3');
                    }else { //이벤트
                        $('#timeline_badge' + index).attr('class', 'timeline-badge warning');
                        $('#timeline_badge' + index).append('<i class="fa fa-star"></i>');
                        $('#timeline_type' + index).attr('class', 'badge badge-pill badge-warning mb-3');

                        if(restaurant.post_img!='') {
                            var img_div =
                                `<div class="text-center m-5">
                                    <img width=200 height=200
                                        src="/media/` + restaurant.post_img + `"
                                        alt="..." class="img-thumbnail">
                                </div>`;
                            $('#timeline_content'+index).append(img_div);
                        }
                    }

                    $('#min_price'+index).append(restaurant.min_price+'원');
                    $('#delivery_charge'+index).append(restaurant.delivery_charge+'원');
                    $('#restaurant_title'+index).html(
                        '<a href="/category/3/restaurant/'+restaurant.restaurant_id+'/">'+restaurant.restaurant_title+'</a>');
                    $('#create_time'+index).html(passing_time(restaurant.created_time));
                    $('#timeline_type'+index).html(restaurant.timeline_type_name);
                    $('#timeline_content'+index).append(restaurant.post_info);
                    $('#restaurant_img'+index).attr('src', '/media/'+restaurant.restaurant_img);

                    if(timeline_type==5){
                        $('#timeline_title'+index).append(`<h6>`+restaurant.yosidy_deadline+`까지</h6>`);
                        $('#timeline_content'+index).append(
                            `<div><a href="/yosigy/`+restaurant.yosigy_id+`/">요식이 식권 이벤트 보러가기</a></div>`)
                    }

                }else {
                    var info_div =
                        `<li class="timeline-inverted">
                            <div class="timeline-badge dark"><i class="fa fa-info"></i></div>            
                            <div class="timeline-panel">
                                <span class="badge badge-pill badge-danger mb-3">
                                    정보 변경
                                </span>
                                <span class="badge badge-pill badge-gray mb-3">
                                    `+restaurant.timeline_type_name+`
                                </span>
                                <span>
                                    <small class="text-muted">
                                        <i class="fa fa-time">&nbsp;`+passing_time(restaurant.created_time)+`</i> 
                                    </small>
                                </span>
                                <div class="timeline-heading">
                           
                                    <p>
                                        <a class="strong font-primary">
                                            <a href="/category/3/restaurant/`+restaurant.restaurant_id+`/">
                                            `+restaurant.restaurant_title+` 
                                            </a>
                                        </strong>
                                        의 `+restaurant.changed_item+`이
                                        <span class="badge badge-pill badge-dark mr-2">
                                            `+restaurant.prior_info+`
                                        </span> 에서
                                        <span class="badge badge-pill badge-dark mr-2">
                                            `+restaurant.post_info+`
                                        </span>
                                        으로 변경되었습니다.
                                    </p>
                                </div>
                            </div>
                        </li>`;
                    restaurant_timeline_div.append(info_div);
                }

                var like_container_div = $('#like_container'+index);
                    if (restaurant.like){
                        like_container_div.append(`<i class="fa fa-heart mr-2" id="like_`+timeline_id+`" 
                            onclick="update_like('`+api_url+`',`+timeline_id+`)"> ` + restaurant.like_count+`</i> `)

                    }else{
                        like_container_div.append(`<i class="fa fa-heart-o mr-2" id="like_`+timeline_id+`" 
                            onclick="update_like('`+api_url+`',`+timeline_id+`)"> ` + restaurant.like_count+`</i> `)

                    }
                    var comment_api_url = api_url+ timeline_id + '/comment/';
                    like_container_div.append(`<i class="fa fa-comment" id="comment_`+timeline_id+`"
                            onclick="show_comment_modal('`+comment_api_url+`', `+timeline_id+`)">`+restaurant.comment_count+`</i>`);
                index++;
            });
        }
    });
}


function update_like(timeline_api_url, timeline_id) {
    var csrftoken = getCookie('csrftoken');
    var api_url = timeline_api_url + timeline_id + '/like/';

    $.ajax({
        type: 'POST',
        url: api_url,
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (data) {
            alert(data.responseJSON['error']);

        },
        success: function (data) {
            var like_div = $('#like_'+timeline_id);

            if(data.like){
                like_div.attr('class', 'fa fa-heart mr-2')

            }else{
                like_div.attr('class', 'fa fa-heart-o mr-2')
            }
            like_div.html(data.like_count)
        }
    });
}

function show_comment_modal(comment_api_url, timeline_id){
    var api_url = comment_api_url;

    var modal_content =
        `<div id="timeline_detail_modal`+timeline_id+`" class="modal fade bd-example-modal-xl" tabindex="-1" role="dialog"
            aria-labelledby="myExtraLargeModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLongTitle"></h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="location.reload()">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="container" id="comment_modal_body_`+timeline_id+`">
                        </div>
                    </div>
                    <div id="comment_post_form">
                        <div class="modal-footer input-group mb-3">
                           <input type="text" class="form-control" id="comment" name="comment" 
                                placeholder="댓글을 입력하세요..." >
                           <div class="input-group-append">
                                <button class="btn btn-outline-secondary" type="button"
                                onclick="post_comment('`+api_url+`',`+timeline_id+`)">게시</button>
                           </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;

    $('#comment_modal_list').append(modal_content);
    $('#timeline_detail_modal'+timeline_id).modal();

    $.ajax({
        type: 'GET',
        url: api_url,
        dataType: 'json',
        error: function (data) {
            $('#comment_modal_body_'+timeline_id).html(data.responseJSON['error']);

        },
        success: function (data) {
            var comments = data.comments;

            var modal_body = '';
            $.each(comments, function(index, comment){
                modal_body +=
                    `
                      <div class="row m-3" id="comment_row_`+comment.id+`">
                          <div class="container">
                                <div class="container">
                                    <strong>`+comment.username+`</strong>
                                    &nbsp;`+comment.comment;

                if(comment.is_my_comment){
                    modal_body +=
                        `
                                        <span class="container-fluid text-right">
                                            <small>
                                                <a class="text-primary"
                                                    onclick="delete_comment('`+api_url+`',`+timeline_id+`,`+comment.id+`)"> 
                                                    삭제  
                                                </a>
                                            </small>
                                        </span>
                        `;
                }
                modal_body +=
                    `
                                </div>
                                
                                <span class="ml-3">
                                    <small class="text-muted">
                                        <i class="fa fa-time"> `+passing_time(comment.created_time)+`</i> 
                                    </small>
                                </span>
                            </div>
                      </div>  
                    `;

            });
            $('#comment_modal_body_'+timeline_id).html(modal_body);
        }
    });
}

function post_comment(comment_api_url, timeline_id){
    var csrftoken = getCookie('csrftoken');
    var api_url = comment_api_url;
    var comment=$('#comment').val();
    var form_data = {
        'comment': comment
    };
    $.ajax({
        type: 'POST',
        url: api_url,
        data: JSON.stringify(form_data),
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (data) {
            if(data.responseJSON['error']['comment']){
                $('#comment').focus()
            }else{
                alert('댓글 입력에 실패했습니다. 다시 한번 입력하세요')
            }

        },
        success: function (data) {
            show_comment_modal(comment_api_url, timeline_id);
            $('#comment').val('');
        }
    });
}

function delete_comment(comment_api_url, timeline_id, comment_id){
    var csrftoken = getCookie('csrftoken');
    var api_url = comment_api_url+comment_id;

    $.ajax({
        type: 'DELETE',
        url: api_url,
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (data) {
            alert(data.responseJSON['error']);

        },
        success: function (data) {
            alert(data.message);
            $('#comment_row_'+comment_id).remove();
        }
    });
}


