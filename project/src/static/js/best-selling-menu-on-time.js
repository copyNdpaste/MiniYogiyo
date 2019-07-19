(function(){
    $.ajax({
        type: "GET",
        url: "/api/timeline/bestmenu/",
        success: bestMenuSuccess,
        error: bestMenuError,
    });
}());

$(document).on('click', '#best-seller', function(){
    $('#img-modal').modal('show');
});

function bestMenuSuccess(data) {
    var html = '';
    var address = data.address;
    var modal = '';

    if(data.order) {
        menu = data.order[0]['menu'];
        menuId = data.order[0]['menu_id'];
        quantity = data.order[0]['menu_quantity'];
        img = data.order[0]['menu__img'];
        cartId = data['cart_id'];
        startHour = data['start_hour'];
        endHour = data['end_hour'];
        html +=
            `<div class="alert alert-primary" role="alert">
                오늘 ` + startHour + `시부터 ` + endHour + `시까지 ` +
                address +
                `에서 `+
                `<button id="best-seller" class="btn btn-primary">` + menu + `</button>
                 ` +
                quantity +
                `개 팔렸습니다 ! !
            </div>`;

        modal += `
        <div class="modal fade" id="img-modal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" 
        aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">` + menu + `</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <img src="/media/` + img + `" alt="` + menu + `" width="300px" height="300px"
                        style="display: block; margin-left: auto; margin-right: auto;"> 
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary"
                        onclick="createCartItem('` + cartId + `', ` + menuId + `)">주문하기</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>`;

        $('#for-img-modal').append(modal);
    }else{
        html +=
            `<div class="alert alert-danger" role="alert">` +
                data.message +
            `</div>`
    }
    $('#best-selling').html(html);
}

function bestMenuError(data) {
    $('#best-selling').html(
        `<div class="alert alert-danger" role="alert">` +
            data.responseJSON.message +
        `</div>`
    );
}
