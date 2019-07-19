(function(){
   $.ajax({
       type: "GET",
       url: "/api/yosigy/ticket/list/",
       success: yosigyTicketListSuccess,
       error: yosigyTicketListError,
   });
}());

function restaurantIdDuplicateCheck(restaurantId){
    var firstRestaurantId = restaurantId[0];
    for(var i=1; i<restaurantId.length; i++){
        if (restaurantId[i] !== firstRestaurantId){
            return false;
        }
    }
    return true;
}

$(document).on('click', '.yosigy-check-btn', function(){
    var checkedYosigy = [];
    var restaurantId = [];
    $('.yosigy-check-box:checked').each(function(i){
        checkedYosigy[i] = $(this).val();
        restaurantId[i] = $(this)[0].dataset.restaurantId;
    });

    restaurantIdCheck = restaurantIdDuplicateCheck(restaurantId);

    if(checkedYosigy.length === 0){
        alert('요식이를 선택해주세요!');
    }else if(restaurantIdCheck){
        window.location.href = "http://127.0.0.1:8000/yosigy/order/list/?yosigy-check=" + checkedYosigy;
    }else{
        alert('같은 레스토랑의 요식이를 선택해주세요 !');
    }
});

function yosigyTicketListSuccess(data){
    yosigyTicketList = data.yosigy_ticket_list;
    yosigyQuantity = data.yosigy_ticket_rest;
    $('#yosigy-quantity').append(
        ' <div class="badge badge-warning">'+yosigyQuantity+'</div>'
    );

    var htmlNotUsed = '';
    var htmlUsed = '';
    var i;
    var recentlyPurchased = 0;
    if (yosigyQuantity > 15) {
         recentlyPurchased = 15;
    }
    var notUsedYosigyTickets = [];
    var usedYosigyTickets = [];

    for(i=0; i<yosigyTicketList.length; i++){
        if(yosigyTicketList[i].status === 2) {
            notUsedYosigyTickets.push(yosigyTicketList[i]);
        }else if(yosigyTicketList[i].status === 3){
            usedYosigyTickets.push(yosigyTicketList[i]);
        }
    }
    htmlNotUsed +=
    `<div class="tab-pane fade show active" id="not-used-yosigy-ticket">
        <div id="not-used-yosigy-ticket-slider"></div>
        <button class="btn btn-primary yosigy-check-btn" style="display:block; width:100%; margin-top:20px;">사용하기</button> 
        <form>
            <div class="row">`;
    for(i=recentlyPurchased; i<notUsedYosigyTickets.length; i++) {
        if(notUsedYosigyTickets[i].status === 2) {
            htmlNotUsed +=
            `<div class="card col-sm-3 padding-zero m-3" style="margin: 0 auto;">
                <div class="card-header">
                    <table>
                    <tr><span class="card-title">` + notUsedYosigyTickets[i].restaurant_title + `</span></tr>
                    <tr>
                    <td><b class="card-title">` + notUsedYosigyTickets[i].menu__name + ` </b></td>
                        <td>
                            <span class="card-subtitle badge badge-primary">사용가능</span>
                        </td>
                        <td>
                            <div class="checkbox">
                                <input name="yosigy-check" class="yosigy-check-box" type="checkbox" value="` + notUsedYosigyTickets[i].pk + `" data-restaurant-id="` + notUsedYosigyTickets[i].restaurant_id + `">
                            </div>
                        </td>
                    </tr>
                    </table>
                </div>
                <div style="margin: 0 auto;">
                    <img style="height: 200px; width: 200px; display: block;" src="/media/` + notUsedYosigyTickets[i].menu__img + `" alt="` + notUsedYosigyTickets[i].menu__name + `">
                </div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">할인된 가격 ` + notUsedYosigyTickets[i].price + `원</li>
                </ul><div class="card-footer text-muted">유효기간: ` + expired_time_calc(notUsedYosigyTickets[i].expire_time) + `</div>
            </div>`;
        }
    }
            htmlNotUsed +=
            `</div>
        </form>
        <button class="btn btn-primary yosigy-check-btn" style="display:block; width:100%; margin-top:20px;">사용하기</button>
    </div>`;

    htmlUsed +=
    `<div class="tab-pane fade" id="used-yosigy-ticket">
        <form>
            <div class="row">`;
    for(i=0; i<usedYosigyTickets.length; i++) {
        if(usedYosigyTickets[i].status === 3) {
            htmlUsed +=
            `<div class="card col-sm-3 padding-zero m-3" style="margin: 0 auto;">
            <div class="card-header">
                <table>
                    <tr><span class="card-title">` + usedYosigyTickets[i].restaurant_title + `</span></tr>
                    <tr>
                        <td><b class="card-title">` + usedYosigyTickets[i].menu__name + ` </b></td>
                        <td><span class="card-subtitle badge badge-dark">사용됨</span></td>
                    </tr>
                </table>
            </div>
                <div style="margin: 0 auto;">
                    <img style="height: 200px; width: 200px; display: block;" src="/media/` + usedYosigyTickets[i].menu__img + `" alt="` + usedYosigyTickets[i].menu__name + `">
                </div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">할인된 가격 ` + usedYosigyTickets[i].price + `원</li>
                </ul><div class="card-footer text-muted">유효기간: ` + expired_time_calc(usedYosigyTickets[i].expire_time) + `</div>
            </div>`;
        }
    }
        htmlUsed +=
            `</div>
        </form>
    </div>`;
    $(document).ready(function(){
        var html2 =
        `<div class="owl-carousel">`;
        for(i=0; i<recentlyPurchased; i++) {
            if(notUsedYosigyTickets[i] && notUsedYosigyTickets[i].status === 2) {
                html2 +=
                `<div class="card col-sm-10 padding-zero m-3" style="margin: 0 auto;">
                    <div class="card-header">
                        <table>
                        <tr><span class="card-title">` + notUsedYosigyTickets[i].restaurant_title + `</span></tr>
                        <tr>
                            <td><b class="card-title">` + notUsedYosigyTickets[i].menu__name + ` </b></td>
                        </tr>
                        <tr>
                            <td>
                                <span class="card-subtitle badge badge-primary">사용가능</span>
                            </td>
                            <td>
                                <div class="checkbox">
                                    <input name="yosigy-check" class="yosigy-check-box" type="checkbox" value="` + notUsedYosigyTickets[i].pk + `" data-restaurant-id="` + notUsedYosigyTickets[i].restaurant_id + `">
                                </div>
                            </td>
                        </tr>
                        </table>
                    </div>
                    <div style="margin: 0 auto;">
                        <img style="height: 150px; width: 150px; display: block;" src="/media/` + notUsedYosigyTickets[i].menu__img + `" alt="` + notUsedYosigyTickets[i].menu__name + `">
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">할인된 가격 ` + notUsedYosigyTickets[i].price + `원</li>
                    </ul><div class="card-footer text-muted">유효기간: ` + expired_time_calc(notUsedYosigyTickets[i].expire_time) + `</div>
                </div>`;
            }
        }
            html2 +=
            `</div>`;
        $('#not-used-yosigy-ticket-slider').append(html2);
         $('.owl-carousel').owlCarousel();
    });
    $('#not-used-or-used').append(htmlNotUsed);
    $('#not-used-or-used').append(htmlUsed);
}

function expired_time_calc(time){
    var expired_time = new Date(time);
    var year = expired_time.getFullYear() + '년';
    var month = expired_time.getMonth() + 1 + '월';
    var day = expired_time.getDate() + '일';
    return year + ' ' + month + ' ' + day + '까지';
}

function yosigyTicketListError(data){
    $('#yosigy-ticket-list').html(
        `<div class="alert alert-danger" role="alert">` +
        data.responseJSON.message +
        `</div>`

    );
}