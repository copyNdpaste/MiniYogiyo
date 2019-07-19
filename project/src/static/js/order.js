function createOrder(cart_id, restaurant_id, user_id, total_price) {
    const csrftoken = getCookie('csrftoken');

    address = $("#address").val()
    address_detail = $("#address2").val()
    phone = $("#phone").val()
    payment = $("label.btn.btn-outline-primary.active")


    if (payment[0].id == 'cash') {
        payment = 0
    } else {
        payment = 1
    }

    var coupon = get_selected_coupon();

    var form_data = {
        "user": user_id,
        "restaurant": restaurant_id,
        "cart": cart_id,
        "total_price": total_price,
        "address": address,
        "address_detail": address_detail,
        "phone_num": phone,
        "payment_status": payment,
        "registered_coupon_id": coupon.id,
        "gift_coupon": coupon.gift_coupon_id
    }

    console.log(form_data)

    $.ajax({
        type: 'POST',
        url: '/api/order/',
        data: JSON.stringify(form_data),
        dataType: 'json',
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (request) {
            console.log(request)
            alert("주문에 실패하였습니다. 주문 정보를 다시 확인해주세요.")
        },
        success: function (data) {
            alert(data.message)
            window.location.href = 'http://127.0.0.1:8000/order/history/'
        }
    });
}

var selected_coupon = '';

function get_selected_coupon() {
    return selected_coupon;
}

function set_selected_coupon(coupon) {
    selected_coupon = coupon;
    console.log(coupon)
}

function testModal(index) {
    $('#myModal-' + index).modal()
}

function reOrder(order_id) {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'POST',
        url: '/api/order/reorder/' + order_id + '/',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (request) {
            alert("재 주문에 실패하였습니다.")
        },
        success: function (data) {
            alert(data.message)
            window.location.href = 'http://127.0.0.1:8000/cart/'
        }
    });
}
