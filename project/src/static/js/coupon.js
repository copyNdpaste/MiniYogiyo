function send_email() {
    $('input[name="receiver_email"]').attr('type', 'text');
    $('input[name="receiver_phone"]').attr('type', 'hidden');

    $('#send_coupon_btn').attr("disabled", false);
}

function send_phone() {
    $('input[name="receiver_email"]').attr('type', 'hidden');
    $('input[name="receiver_phone"]').attr('type', 'text');

    $('#send_coupon_btn').attr("disabled", true);
}

function send_gift_coupon(url){
    var receiver_email = $('input[name="receiver_email"]');
    var receiver_name = $('input[name="receiver_name"]');
    var check_price_radio = $('input:radio[name="price"]').is(':checked');
    var required_html = '* 필수입력사항입니다.';

    if(receiver_name.val()==''){
        receiver_name.focus();
        $('#receiver').html(required_html).css('color','red');

    }else if(receiver_email.val()=='') {
        receiver_email.focus();

    }else {
        $('#receiver').html('');
        var csrftoken = getCookie('csrftoken');
        var form_obj = $('#gift_coupon_form').serializeObject();

        if($('#other_price_input').val()!=undefined) {

            if (check_price_radio) {
                $('#other_price_input').remove();
            }else{
                form_obj['price'] = $('#other_price_input').val();
            }

        }else{
            if(!check_price_radio){
                alert('금액을 선택해 주세요');
                return false;
            }
        }

        var form_data = JSON.stringify(form_obj);

        $.ajax({
            type: 'POST',
            url: url,
            data: form_data,
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            error: function (data) {

                if (data.status == 401) {
                    alert('선물하기는 로그인 후 가능합니다.\n로그인을 먼저 해주세요');

                }else {
                    var email_error = data.responseJSON.error.receiver_email;
                    var price_error = data.responseJSON.error.price;

                    if(email_error!=undefined) {
                        alert(email_error)

                    }else if(price_error!=undefined){
                        alert(price_error);

                    }else{
                        console.log(data.responseJSON['error']);
                        alert('fail')
                    }
                }
            },
            success: function (data) {
                alert(data.message);
                location.reload()
            }
        });
    }
}

function set_coupon_code(){
    var coupon_code_input = $('input[name="coupon_code"]')
    coupon_code = getCookie('coupon_code')
    coupon_code_input.val(coupon_code)
}

function register_coupon(url){
    var csrftoken = getCookie('csrftoken');
    var coupon_code = {
        'coupon_code': $('input[name="coupon_code"]').val()
    };

    coupon_code_cookie=getCookie('coupon_code')
    setCookie('coupon_code', '', -1)

    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(coupon_code),
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (data) {
            if (data.status == 401) {
                alert('선물하기는 로그인 후 가능합니다.\n로그인을 먼저 해주세요')
            } else {
                error_msg = data.responseJSON.error
                alert(error_msg);
                location.href ='/coupon/register_coupon/'
            }
        },
        success: function (data) {
            alert(data.message);
            location.href ='/coupon/register_coupon/'
        }
    });
}

function get_received_coupon_list(api_url){
    var coupon_list_div = $('#received_coupon_list');
    var coupon_div = '';
    var modal_div = '';

    $.ajax({
        type: 'GET',
        url: api_url,
        dataType: 'json',
        error: function (data) {
            if (data.status == 401) {
                alert('내 쿠폰 보기는 로그인 후 가능합니다.\n로그인을 먼저 해주세요')
            }else if(data.status == 404){
                coupon_div += data.responseJSON['message'];
                coupon_list_div.append(coupon_div)
            }else{
                alert('fail')
            }
        },
        success: function (data) {
            var coupons = data.coupons;
            var num = 0;

            coupons.forEach(function(coupon){

                if(coupon.is_available) {
                    coupon_name = '미니 요기요 gift card(' + coupon.price + '원 권)';
                    // 이용가능한 쿠폰
                    coupon_div += '   <div class="card border-danger mb-3" style="max-width: 50rem;">';
                    coupon_div += '       <div class="card-header">';
                    coupon_div += '         <h5>' + coupon.price + '원권';
                    coupon_div += '         &nbsp;<small>from <cite title="Source Title">' + coupon.sender_name + '</cite></small>';
                    coupon_div += '         <button type="button" class="btn btn-primary btn-sm badge-pill"';
                    coupon_div += '          data-toggle="modal" data-target="#handoverModal' + num + '"> 양도하기</button>';
                    coupon_div += '         </h5>';
                    coupon_div += '         <p class="mb-0 text-muted">&nbsp;' + coupon.create_date + '~' + coupon.expire_date + '</p>';
                    coupon_div += '       </div>';
                    coupon_div += '       <div class="card-body">';
                    coupon_div += '           <p class="card-text">상품명: '+ coupon_name +'  <br>';
                    coupon_div += '           유효기간: ~' + coupon.expire_date + '까지<br>';
                    coupon_div += '           gift card 번호: ' + coupon.coupon_code + '';
                    coupon_div += '           </p>';
                    coupon_div += '       </div>';
                    coupon_div += '   </div>';

                    <!-- Modal -->
                    coupon_div += '<div class="modal fade" id="handoverModal' + num + '" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">';
                    coupon_div += '<div class="modal-dialog" role="document">';
                    coupon_div += '    <div class="modal-content" >';
                    coupon_div += '        <div class="modal-header" id="modal_header">';
                    coupon_div += '            <div class="modal-title" id="modal_title">';
                    coupon_div += '              <p class="mb-0">' + coupon_name +'</p>';
                    coupon_div += '              <small>gift card 번호: ' + coupon.coupon_code + '</small>';
                    coupon_div += '            </div>';
                    coupon_div += '            <button type="button" id="close_btn" class="close" data-dismiss="modal" aria-hidden="ture">x</button>';
                    coupon_div += '        </div>';
                    coupon_div += '        <div class="modal-body">';
                    coupon_div += '            <form id="receiver_form">';
                    coupon_div += '                <div class="form-group">';
                    coupon_div += '                  <label>username</label>';
                    coupon_div += '                  <input name="username" type="text" class="form-control"';
                    coupon_div += '                         placeholder="양도해줄 사람의 username">';
                    coupon_div += '                </div>';
                    coupon_div += '                <div class="form-group">';
                    coupon_div += '                  <label>email</label>';
                    coupon_div += '                  <input name="email" type="email" class="form-control"';
                    coupon_div += '                         aria-describedby="emailHelp" placeholder="양도해줄 사람의 email">';
                    coupon_div += '                </div>';
                    coupon_div += '            </form>';
                    coupon_div += '        </div>';
                    coupon_div += '      <div class="modal-footer" id="modal_footer_div">';
                    coupon_div += '        <button type="button" class="btn btn-secondary" data-dismiss="modal">취소</button>';
                    coupon_div += '        <button type="button" class="btn btn-primary"';
                    coupon_div += '           onclick="handover_coupon('+coupon.registered_coupon_id+')">양도하기</button>';
                    coupon_div += '      </div>';
                    coupon_div += '    </div>';
                    coupon_div += '  </div>';
                    coupon_div += '</div>';
                    num++;

                }else{
                    //이용 불가능한 쿠폰
                    coupon_div += '     <div class="card border-light mb-3" style="max-width: 50rem;">';
                    coupon_div += '         <div class="card-header"><h5>';


                    if(!coupon.is_owner){
                        coupon_div +='          <span class="badge badge-dark">양도함</span>&nbsp;';
                    }else if(coupon.is_used){
                        coupon_div +='          <span class="badge badge-info">사용됨</span>&nbsp;';
                    }else if(coupon.is_expired) {
                        coupon_div += '          <span class="badge badge-dark">만료됨</span>&nbsp;';
                    }

                    coupon_div += coupon.price + '원권';
                    coupon_div += '         &nbsp;<small>from <cite title="Source Title">' + coupon.sender_name + '</cite></small></h5>';
                    coupon_div += '         <p class="mb-0 text-muted">&nbsp;' + coupon.create_date + '~' + coupon.expire_date + '</p>';
                    coupon_div += '         </div>';
                    coupon_div += '         <div class="card-body">';
                    coupon_div += '           <p class="card-text">';
                    coupon_div += '             상품명: 미니 요기요 gift card(' + coupon.price + '원 권) <br>';
                    coupon_div += '             유효기간: ~' + coupon.expire_date + '까지<br>';
                    coupon_div += '             gift card 번호: ' + coupon.coupon_code + '';
                    coupon_div += '            </p>';
                    coupon_div += '         </div>';
                    coupon_div += '    </div>';

                }
            });
            coupon_list_div.append(coupon_div);
        }
    });
}

function get_sent_coupon_list(api_url){
    var coupon_list_div = $('#sent_coupon_list');
    var coupon_div ='';

    $.ajax({
        type: 'GET',
        url: api_url,
        dataType: 'json',
        error: function (data) {
            if (data.status == 401) {
                alert('내 쿠폰 보기는 로그인 후 가능합니다.\n로그인을 먼저 해주세요')
            }else if(data.status == 404){
                coupon_div += data.responseJSON['message'];
                coupon_list_div.append(coupon_div);
            }else{
                alert('fail')
            }
        },
        success: function (data) {
            var coupons = data.coupons;

            coupons.forEach(function(coupon) {

                coupon_div += '   <div class="card border-danger mb-3" style="max-width: 50rem;">';
                coupon_div += '       <div class="card-header"><h5>' ;

                if(coupon.is_buyer){
                   coupon_div +='          <span><img src="/static/img/gift.png"></span>&nbsp;';
                }else{
                   coupon_div +='          <span><img src="/static/img/forward.png"></span>&nbsp;';
                }

                coupon_div +=          coupon.price + '원권';
                coupon_div += '         &nbsp;<small>to <cite title="Source Title">' + coupon.receiver_name + '</cite></small>';
                coupon_div += '         </h5>';
                coupon_div += '         <p class="mb-0 text-muted">&nbsp;' + coupon.create_date + '~' + coupon.expire_date + '</p>';
                coupon_div += '       </div>';
                coupon_div += '       <div class="card-body">';
                coupon_div += '           <p class="card-text">상품명: 미니 요기요 gift card(' + coupon.price + '원 권) <br>';
                coupon_div += '           gift card 번호: ' + coupon.coupon_code + '';

                if(coupon.is_used){
                    coupon_div +='          <span class="badge badge-info">사용됨</span>';
                }else if(coupon.is_buyer&coupon.is_registered){
                    coupon_div +='          <span class="badge badge-info">등록됨</span>';
                }
                
                coupon_div += '           </p>';
                coupon_div += '       </div>';
                coupon_div += '   </div>';

            });
            coupon_list_div.append(coupon_div);
        }
    });
}

function get_available_coupon_list(api_url){
    var coupon_list_div = $('#available_coupon_list');
    var coupon_div ='';

    $.ajax({
        type: 'GET',
        url: api_url,
        dataType: 'json',
        error: function (data) {
            if (data.status == 401) {
                alert('내 쿠폰 보기는 로그인 후 가능합니다.\n로그인을 먼저 해주세요');
            }else if(data.status == 404){
                coupon_div += data.responseJSON['message'];
                coupon_list_div.append(coupon_div);
            }else{
                alert('fail')
            }
        },
        success: function (data) {
            var coupons = data.coupons;

            coupons.forEach(function(coupon){
                coupon_div += '   <div class="card border-danger mb-3" style="max-width: 50rem;">';
                coupon_div += '       <div class="card-header">';
                coupon_div += '         <h5>' + coupon.price + '원권';
                coupon_div += '         </h5>';
                coupon_div += '         <p class="mb-0 text-muted">&nbsp;' + time_to_date(coupon.create_date) + '~' + coupon.expire_date + '</p>';
                coupon_div += '       </div>';
                coupon_div += '       <div class="card-body">';
                coupon_div += '           <p class="card-text"> 상품명: 미니 요기요 gift card(' + coupon.price + '원 권) <br>';
                coupon_div += '           유효기간: ~' + coupon.expire_date + '까지<br>';
                coupon_div += '           gift card 번호: ' + coupon.coupon_code + '';
                coupon_div += '           </p>';
                coupon_div += '       </div>';
                coupon_div += '   </div>';
            });
            coupon_list_div.append(coupon_div);
        }
    });
}

function get_coupon_content(coupon){
    var coupon_content ='gift card <strong>' + coupon.price +'원</strong><br><small>(gift card 번호: '+coupon.coupon_code+')</small>';
    return coupon_content
}

var pre_total_price = 0;

function time_to_date(time){
    var time_date = new Date(time);
    return time_date.toISOString().substring(0, 10);
}

function set_available_coupon_list(total_price){
    var coupon_num = 0;
    pre_total_price = total_price;

    $.ajax({
        type: 'GET',
        url: '/api/coupon/available_coupon_list/',
        dataType: 'json',
        error: function (data) {
            if(data.status == 404) {
                $('#coupon_num').append(coupon_num);
                $('#coupon_dropdown').attr('disabled', 'disabled');
            }else{
                alert('fail');
            }
        },
        success: function (data) {
            var coupon_div = $('#available_card_list');
            var coupons = data.coupons;
            var coupon_list='';

            coupon_div.append('<hr>');
            coupons.forEach(function(coupon) {
                var coupon_content = get_coupon_content(coupon);

                coupon_num ++;
                coupon_list = '<a class="dropdown-item" id ="coupon_select_btn' + coupon_num + '">' + coupon_content + '</a><hr>';
                coupon_div.append(coupon_list);

                if(coupon.price <= total_price) {
                    $('#coupon_select_btn'+coupon_num+'').click(function() {
                        select_coupon(coupon);
                    });
                }else{
                    $('#coupon_select_btn'+coupon_num+'').css('color', 'grey');

                }
            });
            $('#coupon_num').append(coupon_num);
        }
    });
}

function select_coupon(coupon){
    set_selected_coupon(coupon)

    var coupon_content = get_coupon_content(coupon);

    $('#selected_coupon').empty();
    $('#selected_coupon').append(coupon_content);

    $('#gift_card_price').empty();
    $('#gift_card_price').append('-￦'+coupon.price);

    var post_total_price = pre_total_price - coupon.price;

    $('#total_price').empty();
    $('#total_price').append('￦'+post_total_price);
}

function cancel_coupon(){
    set_selected_coupon('');

    $('#selected_coupon').empty();
    $('#gift_card_price').empty();

    $('#total_price').empty();
    $('#total_price').append('￦'+pre_total_price);
}

function handover_coupon(registered_coupon_id) {
    var csrftoken = getCookie('csrftoken');
    var form_data = JSON.stringify($('#receiver_form').serializeObject());

    $.ajax({
        type: 'POST',
        url: '/api/coupon/use_coupon/'+registered_coupon_id+'/',
        data: form_data,
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (data) {
            if (data.status == 401) {
                alert('양도하기는 로그인 후 가능합니다.\n로그인을 먼저 해주세요');
            }else{
                alert(data.responseJSON.error);
            }
        },
        success: function (data) {
            msg = data.receiver_name + '에게' + data.coupon_code + data.message;
            alert(msg);

            $('#close_btn').click();
            location.reload();
        }
    });
}

function set_unchecked_coupons(){
    var coupon_index_div = $('#coupon_index');
    var coupon_div = '';

    $('#coupon_title').text('새로 양도 받은 쿠폰');
    var coupons = JSON.parse(sessionStorage.getItem('coupons'));

    if (coupons!=null) {
        coupons.forEach(function (coupon) {
            coupon_div += '   <div class="card border-danger mb-3">';
            coupon_div += '       <div class="card-header">';
            coupon_div += '         <h5>' + coupon.price + '원권';
            coupon_div += '         &nbsp;<small>from <cite title="Source Title">' + coupon.sender_name + '</cite></small>';
            coupon_div += '         </h5>';
            coupon_div += '         <p class="mb-0 text-muted">&nbsp;' + time_to_date(coupon.created_time) + '~' + coupon.expire_date + '</p>';
            coupon_div += '       </div>';
            coupon_div += '       <div class="card-body">';
            coupon_div += '           <p class="card-text">미니 요기요 gift card(' + coupon.price + '원 권)<br>';
            coupon_div += '           유효기간: ~' + coupon.expire_date + '까지<br>';
            coupon_div += '           gift card 번호: ' + coupon.coupon_code + '';
            coupon_div += '           </p>';
            coupon_div += '       </div>';
            coupon_div += '   </div>';
        });
    }
    coupon_div += '<button class="btn btn-primary btn-lg" onclick="location.href=`/coupon/my_coupon/received_coupon/`">확인</button>';
    coupon_index_div.append(coupon_div);

    check_unchecked_coupons()
}

function check_unchecked_coupons(){

    var csrftoken = getCookie('csrftoken');
    var api_url = '/api/coupon/unchecked_coupon_list/';

    var coupons = JSON.parse(sessionStorage.getItem('coupons'));

    if(coupons!=null) {
        $.ajax({
            type: 'PUT',
            url: api_url,
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            error: function (data) {
            },
            success: function (data) {
                sessionStorage.removeItem('coupons');
            }
        });
    }
}

function set_other_price(){
    $('input[name="price"]').prop('checked', false);
    $('label[name="price_lb"]').removeClass('active');

    $('#other_price_btn').attr('class', 'btn btn-outline-primary active');

    var modal_content =
        `<div id="price_input_modal" class="modal fade" tabindex="-1" role="dialog"
            aria-labelledby="myExtraLargeModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLongTitle">금액선택 - <small>다른 금액</small></h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="container">
                            <div> 
                                <div class="d-block my-3">
                                    <div class="row mb-2">5천원~ 10만원까지 선물 가능합니다. </div>
                                        <div class="row form-group"> 
                                            <div class="input-group mb-3">
                                            <input class="form-control" id="other_price" name="price" type="number" required 
                                                min="5000" step="1000" max="100000" placeholder="천원 단위로만 입력가능합니다.">
                                            <div class="input-group-append">
                                                <span class="input-group-text">원</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="reset" class="btn btn-secondary" data-dismiss="modal" onclick="cancel_other_price()">취소</button>
                        <button type="button" class="btn btn-primary" data-dismiss="modal" onclick="confirm_other_price()">확인</button>
                    </div>
                </div>
            </div>
        </div>`;

    $('#price_modal').append(modal_content);
    $('#price_input_modal').modal();
}

function cancel_other_price() {
    $('#other_price_btn').removeClass('active');
    $('#other_price_input').remove();

}

function confirm_other_price(){

    var other_price = $('#other_price').val();
    var other_price_input = $('#other_price_input');

    if(other_price===''){
       $('#other_price_btn').removeClass('active');

    }else {
        $('#other_price_btn').attr('class', 'btn btn-outline-primary active');

        if(other_price_input.val()!=undefined){
            other_price_input.remove();
        }

        $('#gift_coupon_form').append('<input type="hidden" id="other_price_input" value="' + other_price + '">');
    }
}
