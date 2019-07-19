
function getRandomMenuPick(){
  $.ajax({
    url: '/api/random_menu_pick/',
    method: "GET",

    error:function (request) {
      alert("랜덤 메뉴가 없습니다. 취향을 선택해주세요.")
      $("#pills-tabContent").empty()
      $("#pills-tabContent").append(`<div id="warning-message-random-menu"><h1>랜덤 메뉴가 없습니다. 취향을 선택해주세요.</h1></div>`)
    },

    success: function (data) {
      $("#random_menu_pick_div").empty()
      $("#random-menu-container").empty()
      $("#warning-message-random-menu").empty()

      $('.loading').show()

      setTimeout(function(){
        $('.loading').hide()
        var cart_id = data.user.cart_id
  
          //랜덤 메뉴 리스트 부분
        $.each(data.menu, function (key, value) {
      
          var id = value.id;
          var img = value.img;
          var name = value.name;
          var detail = value.detail;
          var price = value.price;
          var restaurant_name = value.restaurant_name;
          var restaurant_delivery_charge = value.restaurant_delivery_charge;
          var restaurant_min_order_price = value.restaurant_min_order_price;

          $("#random-menu-container").append(
              `
              <div class="card">
              <div class="card-footer">
                  <h5>`+ restaurant_name + `</h5> <span class="badge badge-primary">최소 주문 금액 : ` + restaurant_min_order_price + `원</span>
                  <span class="badge badge-info">배달요금 : `+ restaurant_delivery_charge + `원</span>
              </div>
                <img class=" card-img-top" src="`+ img + `"
                    alt="Card image cap">
              <div class="card-body">
                  <h5 class="card-title">`+ name +' - ￦ ' + price + `원</h5>
                  <p class="card-text">`+ detail + `</p>
                  <button onclick="createCartItem('`+ cart_id + `',` + id + `)" class="btn btn-danger btn-block"><i class="fas fa-shopping-cart"></i> 주문표 담기</a>
              </div>
              <div id="cart-bottom`+ "-" + id + `" class="card-footer"></div>
          </div>`
          )
          $.each(value.tastes, function (key, value) {
              var tastes = value
              $("#cart-bottom" + "-" + id).append(
                `<span class="badge badge-pill badge-dark">` + tastes + `</span>&nbsp;`
              )
          })
        })
        }, 1000);
  }
});
}


function getAlreadyEatenRandomMenuPick(){
  $.ajax({
    url: '/api/random_menu_pick/already_eaten/',
    method: "GET",

    error:function (request) {
      alert("주문이 완료된 메뉴가 없습니다.")
      $("#pills-tabContent").empty()
      $("#pills-tabContent").append(`<div id="warning-message-random-menu"><h1> 주문이 완료된 메뉴가 없습니다.</h1></div>`)

    },

    success: function (data) {
      
      $("#random_menu_pick_div").empty()
      $("#random-menu-2-container").empty()
      $("#warning-message-random-menu").empty()

      $('.loading').show()
    
      setTimeout(function(){
        $('.loading').hide()
        var cart_id = data.user.cart_id


        var media_url = "http://127.0.0.1:8000/media/"
        //랜덤 메뉴 리스트 부분
      $.each(data.menu, function (key, value) {
        var id = value.id;
        var img = value.img;
        var name = value.name;
        var detail = value.detail;
        var price = value.price;
        var restaurant_name = value.restaurant_name;
        var restaurant_delivery_charge = value.restaurant_delivery_charge;
        var restaurant_min_order_price = value.restaurant_min_order_price;
        
        $("#random-menu-2-container").append(
          `
          <div class="card">
          <div class="card-footer">
              <h5>`+ restaurant_name + `</h5> <span class="badge badge-primary">최소 주문 금액 : ` + restaurant_min_order_price + `원</span>
              <span class="badge badge-info">배달요금 : `+ restaurant_delivery_charge + `원</span>
          </div>
          <img class=" card-img-top" src="`+ media_url +img + `"
          alt="Card image cap">
          <div class="card-body">
              <h5 class="card-title">`+ name +' - ￦ ' + price + `원</h5>
              <p class="card-text">`+ detail + `</p>
              <button onclick="createCartItem('`+ cart_id + `',` + id + `)" class="btn btn-danger btn-block"><i class="fas fa-shopping-cart"></i> 주문표 담기</a>
          </div>
          <div id="cart-bottom-2`+ "-" + id + `" class="card-footer"></div>
      </div>`


        )
        $.each(value.tastes, function (key, value) {
          var tastes = value
          $("#cart-bottom-2" + "-" + id).append(
            `<span class="badge badge-pill badge-dark">` + tastes + `</span>&nbsp;`
          )
      })
      })
      }, 1000)


  }
});
}