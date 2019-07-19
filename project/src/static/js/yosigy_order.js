function createYosigyOrder(userId, restaurantId, ...yosigyId){
    const csrftoken = getCookie('csrftoken');

    var address = $('#address').val();
    var addressDetail = $('#address2').val();
    var phone = $('#phone').val();

    var form_data = {
        "user": userId,
        "address": address,
        "address_detail": addressDetail,
        "phone_num": phone,
        "yosigy_ticket": yosigyId,
        "restaurant": restaurantId,
    };

    $.ajax({
        type: 'POST',
        url: '/api/yosigy/order/',
        data: JSON.stringify(form_data),
        dataType: 'json',
        contentType: 'application/json',
        beforeSend: function(xhr){
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function(data){
            alert('요식이 주문 완료');
            window.location.href = 'http://127.0.0.1:8000/order/history/'
        },
        error: function(data) {
            alert(data.responseJSON.message);
        }
    });
}