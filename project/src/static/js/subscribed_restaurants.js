$(document).on('click', '.subscribe-cancel', function() {
    const csrftoken = getCookie('csrftoken');
    restaurantId = $(this)[0].dataset.restaurantId;
    $.ajax({
        type: "POST",
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        url: '/api/subscribe/restaurant/' + restaurantId + '/',
        success: subscribedRestaurants,
        dataType: "json",
    });
});

function subscribedRestaurants() {
    $.ajax({
        type: 'GET',
        url: '/api/subscribed_restaurants/',
        success: subscribedRestaurantsSuccess,
    })
}

function subscribedRestaurantsSuccess(data){
    var restaurants = data.subscribed_restaurants;
    var html;
    var restaurantList = '';
    var i;
    restaurantList +=
        `<div class="alert alert-dismissible alert-primary" style="height:50px;">
            <strong>구독 중인 레스토랑 목록</strong>
        </div>
        <div class="row" style="margin:0;">`;
    if (restaurants) {
        for (i = 0; i < restaurants.length; i++) {
            restaurantList +=
                `<div>
            <div>
                <a href="/category/` + restaurants[i].category + `/restaurant/` + restaurants[i].pk + `/">
                    <div class="card border-primary mb-3" style="max-width: 20rem; margin:10px">
                        <div class="card-body" style="margin: 0 5px;">
                            <div>
                                <img src="/media/` + restaurants[i].img + `"
                                alt="` + restaurants[i].title + `"
                                width=100px; height=100px;>
                            </div>
                            <div><div style="margin-top:35px;"><span>` + restaurants[i].title + `</span></div></div>
                        </div>
                    </div>
                </a>
                <div style="margin:auto; width:60%">
                    <button class="btn btn-outline-primary subscribe-cancel" style="width:100%;" data-restaurant-id=` + restaurants[i].pk + `>구독취소</button>
                </div>
            </div>
            </div>`
        }
        restaurantList +=
        `</div>`;
        html = restaurantList;
    }else{
        subscribedRestaurantsEmpty(data);
    }
    $('#subscribed-restaurants').html(html);
}

function subscribedRestaurantsEmpty(data) {
    $('#subscribed-restaurants').html(
        `<div class="alert alert-danger" role="alert">` +
        data.message +
        `</div>`
    )
}
