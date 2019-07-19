function popularMenu(url, ordering){

  $.ajax({
    type:'GET',
    url: url,
    dataType: 'json',
    error: function(data) {
      console.log(data)

    },
    success: function (data) {
      console.log(data)
      ordering = "-" + ordering
      
      $("#popular-menu-tbody" + ordering).empty();

      $.each(data.menu, function (key, value) {
        var rank = value.rank;
        var menu_id = value.id;
        var menu_img = "http://127.0.0.1:8000" + value.img;
        var menu_name = value.name;
        var menu_price = value.price;
        var menu_hit = value.hit;
        var menu_score = value.score;
        var menu_like_count = value.like_count;
        var restaurant_img = "http://127.0.0.1:8000" + value.restaurant_img;
        var restaurant_title = value.restaurant_title;
        var cart_id = value.cart_id;

        $("#popular-menu-tbody" + ordering).append(
          `<tr>
            <td class="text-center">
                <h1>`+ rank +`</h1>
            </td>
            <td class="text-center">
                <div>
                    <i class="fas fa-heart mr-2 fontawsome-font-size">
                        <div class="m-2"><span style="color: #000">`+ menu_like_count +`</span></div>
                    </i>
                </div>
            </td>
            <td class="text-center">
                <div>
                    <i class="fas fa-eye mr-2 fontawsome-font-size">
                        <div class="m-2"><span style="color: #000">`+ menu_hit +`</span></div>
                    </i>
                </div>
            </td>
            <td class="text-center">
                <div>
                    <i class="fas fa-star mr-2 fontawsome-font-size">
                        <div class="m-2"><span style="color: #000">`+ menu_score +`</span></div>
                    </i>
                </div>
            </td>
            <td class="text-center">
                <div class="text-center">
                    <img width=100 height=100
                        src="`+ restaurant_img +`"
                        alt="">
                    <a href="#" class=" text-center user-link">`+ restaurant_title +`</a>
                </div>
            </td>
            <td>
                <div class="text-center">
                    <img width=100 height=100
                        src="`+ menu_img +`"
                        alt="">
                    <a href="#" class=" text-center user-link">`+ menu_name +`</a>
                </div>
            </td>
            <td class="text-center">
                <span class="label label-default">￦ `+ menu_price +`원</span>
            </td>
            <td class="text-center">
                <button onclick="createCartItem('`+ cart_id + `',` + menu_id + `)" class="btn btn-danger"><i class="fas fa-shopping-cart"></i>
                    주문표 담기
                </button>
            </td>
          </tr>`
        );



      })
    }
  })

}