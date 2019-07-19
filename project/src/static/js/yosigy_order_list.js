(function(){
    var yosigyPks = $('#yosigy-pks').val();
    $.ajax({
        type: "GET",
        url: "/api/yosigy/order/list/",
        success: yosigyOrderListSuccess,
        error: yosigyOrderListError,
        data: {
            'yosigyPks': yosigyPks,
        },
    });
}());

function yosigyOrderListSuccess(data){
    var yosigyOrderInfo = data.yosigy_order_info;
    var userInfo = data.user_info;
    var yosigyId = [];
    var restaurantId = yosigyOrderInfo[0].restaurant_id;
    var restaurantTitle = yosigyOrderInfo[0].restaurant_title;

    $('#yosigy-order-info').append(`<h1><i class="fas fa-credit-card"></i> ` + userInfo.username + ` 님의 배달주문 결제 </h1><hr>`);

    $('#cart-item-table').append(
        `
        <hr>
        <h5>`+ restaurantTitle + `</h5>
        <hr>
        `
    );

    $('#address-main').append(
        `<input type="text" value="` + userInfo.address + `" class="form-control" id="address"
        placeholder="배달 받으실 주소를 적어주세요." required>`
    );

    $('#address-detail').append(
        `<input type="text" value="` + userInfo.address_detail + `" class="form-control" id="address2" placeholder="주문자의 상세주소를 적어주세요.">`
    );

    $('#user-phone').append(
        `<input type="text" value="`+ userInfo.phone +`" class="form-control" id="phone"
        placeholder="주문자의 전화번호를 적어주세요.">`
    );

    for(var i=0; i<yosigyOrderInfo.length; i++){
        yosigyId.push(yosigyOrderInfo[i].yosigy_id);
        $("#cart-item-list").append(
            `<li class="list-group-item d-flex justify-content-between lh-condensed">
                <div>
                    <img src="/media/`+ yosigyOrderInfo[i].menu_img + `" alt="`+ yosigyOrderInfo[i].menu_name +`" width=80px height=80px class="img-thumbnail">
                        <h6 class="my-0">`+ yosigyOrderInfo[i].menu_name +`</h6>
                        <small class="text-muted">`+ yosigyOrderInfo[i].menu_detail + `</small>
                </div>
                <span class="text-muted">￦ `+ yosigyOrderInfo[i].price + `</span>
            </li>`
        )
    }
    $("#yosigy-order-button").append(
        `<button onclick="createYosigyOrder(` + userInfo.id + "," + restaurantId +  "," + yosigyId + `)" class="btn btn-primary btn-lg btn-block">주문하기</button>`
    )

}

function yosigyOrderListError(data){
    $('#yosigy-order-main').html(
        `<div class="alert alert-danger" role="alert">` +
        data.responseJSON.message +
        `</div>`
    )
}