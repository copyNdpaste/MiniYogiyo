$(document).ready(function () {
    let mypage_div = $('#mypage_div');

    mypage_div.ready(function () {
        if (!(mypage_div.val() == undefined)) {
            get_user_info();
        }
    });

     get_unchecked_coupon()
});

jQuery.fn.serializeObject = function () {
    let result = {};
    let extend = function (i, element) {
        let node = result[element.name];
        if ("undefined" !== typeof node && node !== null) {
            if ($.isArray(node)) {
                node.push(element.value)
            } else {
                result[element.name] = [node, element.value];
            }
        } else {
            result[element.name] = element.value;
        }
    };

    $.each(this.serializeArray(), extend);
    return result
};

function passing_time(created_time) {
    var min = 60 * 1000;
    var now = new Date()
    var datetime = new Date(created_time);
    var minsAgo = Math.floor((now - datetime) / (min));

    var result = {
        'raw': datetime.getFullYear() + '-' + (datetime.getMonth() + 1 > 9 ? '' : '0') +
            (datetime.getMonth() + 1) + '-' + (datetime.getDate() > 9 ? '' : '0') +  datetime.getDate() +
            ' ' + (datetime.getHours() > 9 ? '' : '0') +  datetime.getHours() + ':' + (datetime.getMinutes() > 9 ? '' : '0') +
            datetime.getMinutes() + ':'  + (datetime.getSeconds() > 9 ? '' : '0') +  datetime.getSeconds(),
        'formatted': '',
    };
    if(minsAgo < 1) {
        result.formatted = '방금';
    }else if (minsAgo < 60) { // 1시간 내
        result.formatted = minsAgo + '분 전';
    } else if (minsAgo < 60 * 24) { // 하루 내
        result.formatted = Math.floor(minsAgo / 60) + '시간 전';
    } else { // 하루 이상
        result.formatted = Math.floor(minsAgo / 60 / 24) + '일 전';
    };

    return result.formatted;
}

function getCookie(name) {
    let cookies = document.cookie;

    let cookie = cookies.split(';')
        .map(c => c.trim())
        .filter(c => c.startsWith(name + '='));

    if (cookie.length == 0) {
        return null;
    }

    return decodeURIComponent(cookie[0].split('=')[1]);
}

function setCookie(name, value, day){
    var expire = new Date();
    expire.setDate(expire.getDate() + day);
    cookies = name + '=' + escape(value) + '; path=/ ';
    if(typeof day != 'undefined') cookies += ';expires=' + expire.toGMTString() + ';';
    document.cookie = cookies;
}


function logout() {

    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'GET',
        url: '/api/accounts/logout/',
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('csrftoken', csrftoken);
        },
        error: function (data) {
            alert(data);
        },
        success: function (data) {
            sessionStorage.clear()

            alert(data.message);
            location.reload();
        }
    });
}

function get_user_info() {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'GET',
        url: '/api/accounts/my_page/',
        dataType: 'json',
        error: function (data) {
            alert('fail');
            history.back();
        },
        success: function (data) {
            subscribedRestaurants(data.user_id);
            $('#username').val(data.username);
            $('#email').val(data.email);
            $('input[name="phone"]').val(data.phone);
            $('input[name="address"]').val(data.address);
            $('input[name="address_detail"]').val(data.address_detail);

            let tastes_div = $('#taste_check');
            let tastes_html = '';
            i = 0;
            data.tastes.forEach(function (taste) {
                tastes_html += '<div class="form-check">';
                tastes_html += '<label class="form-check-label">';
                tastes_html += '<input class="form-check-input" type="checkbox" name="tastes" value="' + taste.id + '"';
                tastes_html += (taste.checked ? 'checked' : '') + '>';
                tastes_html += taste.name;
                tastes_html += '</label>';
                tastes_html += '</div>';
                i++;

            });
            tastes_div.html(tastes_html)
        }
    });
}


function update_form(app_name, form_name) {
    const csrftoken = getCookie('csrftoken');
    let form_data = JSON.stringify($('#' + form_name + '_form').serializeObject());
    let url = '/api/' + app_name + '/' + form_name + '/';

    $.ajax({
        type: 'PUT',
        url: url,
        data: form_data,
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (data) {
            alert('fail');
        },
        success: function (data) {
            alert(data.message);
            location.reload()
        }
    });
}

function get_unchecked_coupon(){
    var api_url = '/api/coupon/unchecked_coupon_list/';
    var received_coupon_num_span = $('#received_coupon_num');
    var coupon_btn=$('#btn_coupon_index');

    $.ajax({
        type: 'GET',
        url: api_url,
        dataType: 'json',
        error: function (data) {
            coupon_btn.click(function(){
                location.href = '/coupon/gift_coupon/';
            })
        },
        success: function (data) {
            if(data.coupons!='') {
                received_coupon_num_span.empty();

                var coupons = data.coupons;
                var coupon_num = coupons.length;

                received_coupon_num_span.append(coupon_num);

                sessionStorage.setItem('coupons', JSON.stringify(coupons));

                coupon_btn.click(function () {
                    location.href = '/coupon/my_coupon/';
                });
            }else{
                sessionStorage.removeItem('coupons');
                received_coupon_num_span.empty();

                coupon_btn.click(function(){
                    location.href = '/coupon/gift_coupon/';
                })
            }
        }
    });
}
