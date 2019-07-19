$(document).on('click', '#menu-time-line', function(){
    $.ajax({
        type: "GET",
        url: "/api/timeline/menutimeline/",
        success: menuTimeLineSuccess,
    });
});

function menuTimeLineSuccess(data){
    if(data.message){
        $('#menu-alarm').html(
            `<div class="alert alert-danger" role="alert">` +
                data.message +
            `</div>`
        );
    }else {
        var menuTimelineStatus = {
            CREATE: 1,
            UPDATE: 2,
        };
        var cartId = data.cart_id;
        var menuTimelineInfos = data.menutimeline;
        var i;
        var html = '';
        html +=
            `<div class="container">
            <div class="page-header mt-4">
                <h1 id="timeline">메뉴 알림</h1>
            </div>
            <ul class="timeline">`;
        for (i = 0; i < menuTimelineInfos.length; i++) {
            if (menuTimelineInfos[i].status === menuTimelineStatus.CREATE) {
                html += timeLineCreate(cartId, menuTimelineInfos[i]);
            } else if (menuTimelineInfos[i].status === menuTimelineStatus.UPDATE) {
                html += timeLineUpdate(cartId, menuTimelineInfos[i]);
            }
        }
        html +=
            `</ul>
        </div>
        <div id="menu_comment_modal_list"></div>`;
        $('#menu-alarm').html(html);
    }
}

function timeLineCreate(cartId, menuTimelineInfos){
    var htmlCreate = '';
    var isYosigy = menuTimelineInfos.post_menu_is_yosigy;
    var isSetMenu = menuTimelineInfos.post_menu_is_set_menu;
    var create = '';
    var timeline_id = menuTimelineInfos.timeline_id;
    var api_url = '/api/timeline/menutimeline/';
    var comment_api_url= api_url+timeline_id+'/comment/';

    if(isYosigy){
        create = '요식이 메뉴 추가';
    }else if(isSetMenu){
        create = '요식이 세트 메뉴 추가';
    }else{
        create = '신메뉴 추가';
    }

    htmlCreate +=
    `<li>
        <div class="timeline-badge info"><i class="fa fa-plus"></i></div>
        <div class="timeline-panel">
            <div class="timeline-heading">
                <div class="row">
                    <span class="badge badge-pill badge-primary mr-2">
                        최소주문 금액 : ` + menuTimelineInfos.min_order_price + `원
                    </span>
                    <span class="badge badge-pill badge-info">
                        배달 요금 : ` + menuTimelineInfos.delivery_charge + `원
                    </span>
                </div>
                <div class="row align-items-center">
                    <div class="m-3">
                        <img src="` + menuTimelineInfos.restaurant_img + `"
                            alt="` + menuTimelineInfos.restaurant_title + `" width=80px height=80px>
                    </div>
                    <h5 class="timeline-title">` + menuTimelineInfos.restaurant_title + `</h5>
                </div>
                <span><small class="text-muted"><i class="fa fa-time"></i>` + menuTimelineInfos.created_time + `에 작성되었습니다.</small>
                </span>
            </div>
            <hr>
            <span class="badge badge-pill badge-info  mb-3">
                ` + create + `
            </span>
            <span class="badge badge-pill badge-dark  mb-3">
                ￦ ` + menuTimelineInfos.post_menu_price + `
            </span>

            <h4>` + menuTimelineInfos.menu_name + ` 추가되었습니다.</h4>
            <div class="timeline-body">
                <div class="text-center m-5">
                    <img width=200 height=200
                        src="` + menuTimelineInfos.post_menu_img + `"
                        alt="` + menuTimelineInfos.menu_name + `" class="img-thumbnail">
                </div>

                <div>
                    <p class="font-weight-bold">` + menuTimelineInfos.post_menu_detail + `</p>
                    <div class="row">`;
                        if(isYosigy || isSetMenu){
                            htmlCreate +=
                            `<button class="btn btn-danger btn-block" id="yosigy-buy-button" data-yosigy-id="`+ menuTimelineInfos.yosigy_id +`">
                            <i class="fas fa-shopping-cart"></i>요식이 구매하기</button>`;
                        }else{
                            htmlCreate +=
                            `<button class="btn btn-danger btn-block" onclick="createCartItem('` + cartId + `',` +
                            menuTimelineInfos.menu_id + `)"><i class="fas fa-shopping-cart"></i>주문표 담기</button>`;
                        }
                    htmlCreate += `
                    </div>
                </div>
            </div>
            <hr>`;
            for(var j=0; j<menuTimelineInfos.tastes.length; j++){
                htmlCreate +=
                    `<span class="badge badge-pill badge-dark">` +
                        menuTimelineInfos.tastes[j] +
                    `</span> `;
            }
            htmlCreate += `<hr>
            <div class="row">
                <div class="container">
            `;

            if(menuTimelineInfos.like){
                htmlCreate += `<i class="fa fa-heart mr-2" id="like_`+menuTimelineInfos.timeline_id+`" 
                                onclick="update_menu_like('`+api_url+`',`+timeline_id+`)">` + menuTimelineInfos.like_count + `</i>`

            }else{
                htmlCreate += `<i class="fa fa-heart-o mr-2" id="like_`+menuTimelineInfos.timeline_id+`"
                                onclick="update_menu_like('`+api_url+`',`+timeline_id+`)">` + menuTimelineInfos.like_count + `</i>`
            }

            htmlCreate += `
                    <i class="fa fa-comment" id="comment_`+timeline_id+`"
                    onclick="show_menu_comment_modal('`+comment_api_url+`', `+timeline_id+`)"> ` + menuTimelineInfos.comment_count +`</i>
                </div>
            </div>
        </div>
    </li>
    <li class="timeline">
        <div class="timeline-badge dark"><i class="fa fa-info"></i></div>
        <div class="timeline-panel">
            <span class="badge badge-pill badge-danger mb-3">
                ` + create + `
            </span>
            <span class="badge badge-pill badge-gray mb-3">
                안내
            </span>
            <div class="timeline-heading">
                <p>
                    <strong class="strong font-primary">`+ menuTimelineInfos.restaurant_title +`</strong>의
                    <strong class="strong font-primary">` +
                        menuTimelineInfos.menu_name +
                    `</strong> 출시되었습니다 !
                </p>
            </div>
        </div>
    </li>`;
    return htmlCreate;
}

function timeLineUpdate(cartId, menuTimelineInfos){
    var htmlUpdate = '';
    var updatedInfo = '';
    var currentMenu = menuTimelineInfos.menu_name;
    var update = '메뉴 갱신';
    var isYosigy = menuTimelineInfos.post_menu_is_yosigy;
    var isSetMenu = menuTimelineInfos.post_menu_is_set_menu;
    var timeline_id = menuTimelineInfos.timeline_id;
    var api_url = '/api/timeline/menutimeline/';
    var comment_api_url= api_url+timeline_id+'/comment/';

    htmlUpdate +=
    `<li class="timeline-inverted">
        <div class="timeline-badge danger"><i class="fas fa-exchange-alt"></i></div>
        <div class="timeline-panel">
            <div class="timeline-heading">
                <div class="row">
                    <span class="badge badge-pill badge-primary mr-2">
                        최소주문 금액 : ` + menuTimelineInfos.min_order_price + `원
                    </span>
                    <span class="badge badge-pill badge-info">
                        배달 요금 : ` + menuTimelineInfos.delivery_charge + `원
                    </span>
                </div>
                <div class="row align-items-center">
                    <div class="m-3">
                        <img src="` + menuTimelineInfos.restaurant_img + `"
                            alt="` + menuTimelineInfos.restaurant_title + `" width=80px height=80px>
                    </div>
                    <h5 class="timeline-title">` + menuTimelineInfos.restaurant_title + `</h5>
                </div>
                <span><small class="text-muted"><i class="fa fa-time"></i>` + menuTimelineInfos.created_time + `에 작성되었습니다.</small>
                </span>
            </div>
            <hr>
            <span class="badge badge-pill badge-danger mb-3">
                ` + update + `
            </span>
            <span class="badge badge-pill badge-dark  mb-3">
                ￦ ` + menuTimelineInfos.post_menu_price + `
            </span>
            <h4>` + currentMenu + `</h4>
            <div class="timeline-body">
                <div class="text-center m-5">
                    <img width=200 height=200
                        src="` + menuTimelineInfos.post_menu_img + `"
                        alt="` + currentMenu + `" class="img-thumbnail">
                </div>
                <div>
                    <p class="font-weight-bold">` + menuTimelineInfos.post_menu_detail + `</p>
                    <div class="row">`;
                        if(isYosigy || isSetMenu){
                            htmlUpdate +=
                            `<button class="btn btn-danger btn-block" id="yosigy-buy-button" data-yosigy-id="`+ menuTimelineInfos.yosigy_id +`">
                            <i class="fas fa-shopping-cart"></i>요식이 구매하기</button>`;
                        }else{
                            htmlUpdate +=
                            `<button class="btn btn-danger btn-block" onclick="createCartItem('` + cartId + `',` +
                            menuTimelineInfos.menu_id + `)"><i class="fas fa-shopping-cart"></i>주문표 담기</button>`;
                        }
                htmlUpdate +=
                    `</div>
                </div>
            </div>
            <hr>`;
            for(var j=0; j<menuTimelineInfos.tastes.length; j++){
                htmlUpdate +=
                    `<span class="badge badge-pill badge-dark"> ` +
                        menuTimelineInfos.tastes[j] +
                    `</span> `;
            }
            htmlUpdate += `<hr>
            <div class="row">
                <div class="container">`;


            if(menuTimelineInfos.like){
                htmlUpdate += `<i class="fa fa-heart mr-2" id="like_`+timeline_id+`"
                                onclick="update_menu_like('`+api_url+`',`+timeline_id+`)">` + menuTimelineInfos.like_count + `</i>`

            }else{
                htmlUpdate += `<i class="fa fa-heart-o mr-2" id="like_`+timeline_id+`"
                                onclick="update_menu_like('`+api_url+`',`+timeline_id+`)">` + menuTimelineInfos.like_count + `</i>`
            }
            htmlUpdate +=`
                    <i class="fa fa-comment" id="comment_`+timeline_id+`"
                            onclick="show_menu_comment_modal('`+comment_api_url+`', `+timeline_id+`)">` + menuTimelineInfos.comment_count + `</i>
                </div>
            </div>
        </div>
    </li>
    <li class="timeline-inverted">
        <div class="timeline-badge dark"><i class="fa fa-info"></i></div>
        <div class="timeline-panel">
            <span class="badge badge-pill badge-danger mb-3">
                ` + update + `
            </span>
            <span class="badge badge-pill badge-gray mb-3">
                안내
            </span>
            <strong class="strong font-primary">` + currentMenu + `</strong>`;
            if(menuTimelineInfos.prior_menu_price){
                priorPrice = `￦` + menuTimelineInfos.prior_menu_price;
                postPrice = `￦` + menuTimelineInfos.post_menu_price;
                htmlUpdate += menuUpdated(updatedInfo, currentMenu, priorPrice, postPrice);
            }
            if(menuTimelineInfos.prior_menu_detail){
                priorDetail = menuTimelineInfos.prior_menu_detail;
                postDetail = menuTimelineInfos.post_menu_detail;
                htmlUpdate += menuUpdated(updatedInfo, currentMenu, priorDetail, postDetail);
            }
            if(menuTimelineInfos.prior_menu_img){
                menuName = menuTimelineInfos.menu_name + `</strong>의 이미지가`;
                priorImg = menuTimelineInfos.prior_menu_img;
                postImg = menuTimelineInfos.post_menu_img;
                isImg = true;
                htmlUpdate += menuUpdated(updatedInfo, currentMenu, priorImg, postImg, isImg);
            }
        htmlUpdate +=
        `</div>
    </li>`;

    return htmlUpdate;
}

function menuUpdated(updatedInfo, currentMenu, priorInfo, postInfo, isImg){
    if(isImg){
        updatedInfo +=
        `<div class="timeline-heading">
            <p>
                <div class="text-center m-5">
                    <img src="`+ priorInfo +`" alt="`+ currentMenu +`" width="200px" height="200px" class="img-thumbnail">에서
                </div>
                <div class="text-center m-5">
                    <img src="`+ postInfo +`" alt="`+ currentMenu +`" width="200px" height="200px" class="img-thumbnail">으로 
                </div>변경되었습니다.
            </p>
        </div>`;
        return updatedInfo;
    }else{
        updatedInfo +=
        `<div class="timeline-heading">
            <p>
                <span class="badge badge-pill badge-dark mr-2">` +
                    priorInfo +
                    `</span> 에서
                <span class="badge badge-pill badge-dark mr-2">` +
                    postInfo +
                    `</span>
                으로 변경되었습니다.
            </p>
        </div>`;
        return updatedInfo;
    }
}

$(document).on('click', '#yosigy-buy-button', function(){
    var yosigyPk = $(this)[0].dataset.yosigyId;
    location.href = "http://127.0.0.1:8000/yosigy/"+ yosigyPk +"/";
});

function show_menu_comment_modal(comment_api_url, timeline_id){
    var api_url = comment_api_url;

    var modal_content =
        `<div id="timeline_detail_modal`+timeline_id+`" class="modal fade bd-example-modal-xl" tabindex="-1" role="dialog"
            aria-labelledby="myExtraLargeModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLongTitle"></h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="update_comment_num('`+comment_api_url+`')">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="container" id="comment_modal_body_`+timeline_id+`">
                        </div>
                    </div>
                    <div id="menu_comment_post_form">
                        <div class="modal-footer input-group mb-3">
                           <input type="text" class="form-control" id="menu_comment" name="comment" 
                                placeholder="댓글을 입력하세요..." >
                           <div class="input-group-append">
                                <button class="btn btn-outline-secondary" type="button"
                                onclick="post_menu_comment('`+api_url+`',`+timeline_id+`)">게시</button>
                           </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;

    $('#menu_comment_modal_list').append(modal_content);
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
                                                    onclick="delete_menu_comment('`+api_url+`',`+timeline_id+`,`+comment.id+`)"> 
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

function post_menu_comment(comment_api_url, timeline_id){
    var csrftoken = getCookie('csrftoken');
    var api_url = comment_api_url;
    var comment=$('#menu_comment').val();
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
            console.log(data.responseJSON['error'])
            if(data.responseJSON['error']['comment']){
                $('#menu_comment').focus()
            }else{
                alert('댓글 입력에 실패했습니다. 다시 한번 입력하세요')
            }

        },
        success: function (data) {
            show_menu_comment_modal(comment_api_url, timeline_id);
            $('#menu_comment').val('');
        }
    });
}

function delete_menu_comment(comment_api_url, timeline_id, comment_id){
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

function update_menu_like(timeline_api_url, timeline_id) {
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

function update_comment_num(comment_api_url){
    $.ajax({
        type: 'GET',
        url: comment_api_url,
        dataType: 'json',
        error: function (data) {
            alert(data.responseJSON['error']);

        },
        success: function (data) {
            $('#comment_'+data.timeline_id).html(data.comment_count);
        }
    });
}
