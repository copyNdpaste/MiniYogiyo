function get_ticket_payment_history_tab(api_url){

    $.ajax({
        type: 'GET',
        url: api_url,
        dataType: 'json',
        error: function (data) {
            alert(data.responseJSON.error);

        },
        success:function(data){
            var ticket_payment_history_list = ``;
            var ticket_payments = data.ticket_payments;
            var sliderStart = 0;
            var sliderEnd = 5;
            var ticket_payments_slider = ticket_payments.slice(sliderStart, sliderEnd);

            $('#recently-purchased').html('<h3>최신 구매한 요식이 티켓</h3>');
            $(document).ready(function(){
                var html =
                    `<div class="owl-carousel">`;
                        ticket_payments_slider.slice(0, 5).forEach(function(payment){
                            html +=
                                `<div class="card" style="width:13rem;">
                                    <div class="card-body">
                                        <h5 class="card-title">`+ payment.restaurant_name +`</h5>
                                    </div>
                                    <img src="/media/`+payment.restaurant_img+`" class="card-img-top" alt="`+payment.restaurant_name+`" height="100px">
                                    <div class="card-body">
                                        <ul class="list-group list-group-flush">
                                            <li class="list-group-item">총 가격: `+ payment.total_price +`원</li>
                                            <li class="list-group-item">요식이 티켓: `+ payment.ticket_count +`개</li>
                                        </ul>
                                        <p class="card-text"></p>
                                        <p class="card-text"></p>
                                        <div style="text-align:center;">
                                        <button onclick="get_ticket_payment_history_detail('`+api_url+payment.id+`',`+ payment.id+`)" class="btn btn-primary">
                                            상세보기
                                        </button>
                                        </div>
                                    </div>
                                </div>`;
                            });
                    html +=
                    `</div>`;
                $('#yosigy-ticket-slider').html(html);

                $('.owl-carousel').owlCarousel();
            });

            $('#ticket_payment_headline').html(`<h1>`+data.username+`님의 티켓 구매 내역입니다.</h1>`);

            ticket_payments.forEach(function(payment){
                ticket_payment_history_list +=
                    `<tr>
                        <td>
                            <img src="/media/`+ payment.restaurant_img + `" alt="">
                            <a href="#" class="user-link">`+ payment.restaurant_name + `</a>
                        </td>
                        <td>
                            `+ payment.created_time + `
                        </td>
                        <td class="text-center">
                            <span class="label label-default">`+ payment.ticket_count + `</span>
                        </td>
                        <td class="text-center">
                            ￦ `+ payment.total_price + `원
                        </td>
                        <td class="text-center">
                            <button onclick="get_ticket_payment_history_detail('`+api_url+payment.id+`',`+ payment.id+`)" class="btn btn-primary">
                                상세보기
                            </button>
                        </td>
                    </tr>`;

            });

           $('#ticket_payment_tbody').html(ticket_payment_history_list);

        }
    });
}

function get_ticket_payment_history_detail(api_url, ticket_payment_id){

    $.ajax({
        type: 'GET',
        url: api_url,
        dataType: 'json',
        error: function (data) {
            alert(data.responseJSON.error);

        },
        success:function(data){
            var modal_content =
                `<div id="payment_detail_modal`+ticket_payment_id+`" class="modal fade bd-example-modal-xl" tabindex="-1" role="dialog"
                    aria-labelledby="myExtraLargeModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-xl">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="exampleModalLongTitle">구매 상세 내역</h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <div class="container">
                                    <div class='col-10 offset-1'> 
                                        <h4 class="mb-3">1. 결제 정보</h4>
                                        <hr>
                                        <div class="d-block my-3">
                                            <h5>
                                                <img src="/media/`+ data.restaurant_img + `" 
                                                alt="" width=80px height=80px class="img-thumbnail">
                                                `+ data.restaurant_name + `
                                            </h5>
                                            <span> 
                                               결제 일시: `+data.created_time+` <br>
                                               총 결제 금액: ￦`+data.total_price+` <br>
                                            </span>
                                            
                                        </div>
                                        
                                        <div class="row"></div>
                                                                                                                     
                                        <div class="mb-3">
                                            <h4 class="d-block my-3">2. 구매한 티켓 정보</h4>
                                            <hr>   
                                        </div>
                                        <ul id="ticket_list_`+data.id+`" class="list-group mb-3"> </ul>
                                        
                                        <div class="mb-3">
                                            <h5><p class="pull-right">총 결제금액 : ￦ `+ data.total_price + `</p></h5>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-primary use-yosigy" data-dismiss="modal">사용하기</button>
                                <button type="button" class="btn btn-secondary" data-dismiss="modal">닫기</button>
                            </div>
                        </div>
                    </div>
                </div>`;

            $('#payment_modal_list').html(modal_content);

            data.yosigy_tickets.forEach(function(ticket){
                var ticket_div =
                 `<li class="list-group-item d-flex justify-content-between lh-condensed">
                    <div>
                        <img src="/media/`+ticket.menu_img+`" 
                            alt="..." width="80px" height="80px" class="img-thumbnail">
                        <h6 class="my-0">`+ ticket.ticket_menu + `</h6> 
                        <small class="text-muted">￦`+ ticket.ticket_menu_price + `</small>
                    </div>
                    <h5><strike> ￦` + ticket.menu_price + `</strike> -> ￦ ` + ticket.ticket_menu_price + `</h5>
                </li>`;

                $('#ticket_list_'+data.id).append(ticket_div);
            });

            $('#payment_detail_modal'+ticket_payment_id).modal();
        }
    });
}

$(document).on('click', '.use-yosigy', function(){
    window.location.replace('http://127.0.0.1:8000/accounts/my_page/?tab=2');
});