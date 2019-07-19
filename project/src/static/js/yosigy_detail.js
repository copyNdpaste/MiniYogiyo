selected_yosigy_menu = {}

function create_yosigy_ticket(restaurant_id) {
    const csrftoken = getCookie('csrftoken');
    let url = '/api/yosigy/ticket/' + restaurant_id + '/'
    let yosigy_menu = Object.values(selected_yosigy_menu)

    if (Object.values(selected_yosigy_menu).length === 0) {
        alert("선택한 메뉴가 없습니다.")
        return 0;
    }

    let is_create = confirm("요식이 e-ticket을 구매하시겠습니까?");

    if (!is_create) {
        alert('구매가 취소되었습니다.')
        return 0;
    }

    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(yosigy_menu),
        dataType: 'json',
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },

        error: function (data) {
            let errorObj = JSON.parse(String(data.responseText))
            if (!errorObj.message) {

                alert(errorObj.error.discounted_price)
            }
            alert(errorObj.message)
        }

        ,
        success: function (data) {
            alert('쿠폰 결제에 성공하였습니다.')
            window.location.replace('http://127.0.0.1:8000/accounts/my_page/?tab=2');
        }
    });
}

function append_yosigy_menu(yosigy_menu_id, img_url, id, name, quantity, discounted_price) {
    if (Object.keys(selected_yosigy_menu).length === 0) {
        $("#yosigy-menu-main").append(
            `
            <div id="yosigy-menu-detail-table">
            <table  class="table table-hover text-center">
            <thead>
            <tr>
                <th scope="col">이미지</th>
                <th scope="col">메뉴명</th>
                <th scope="col">단품 가격</th>
                <th scope="col">개수</th>
                <th scope="col">단품가격 X 개수</th>
                <th scope="col">취소</th>
            </tr>
            </thead>
            <tbody id="yosigy-detail-menu-table"></tbody>
        </table>
        <hr>
        <div id="yosigy-menu-total-price" class="m-2 text-right">
             <span class="badge badge-dark"><h4>총 가격: 0원</h4></span>
        </div>
        </div>
            `
        )
    } else {
        if (selected_yosigy_menu[id] !== undefined) {
            alert("메뉴가 중복 됩니다.")
            return 0
        }
    }

    var decoded_name = decodeURIComponent(name)

    var menu_item =
        `<tr id="yosigy-menu-` + id + `">
            <td><img width="80" height="80" src="http://127.0.0.1:8000/media/` + img_url + `" alt=""></td>
            <td>` + decoded_name + `</td>
            <td>` + discounted_price + `</td>
            <td id="yosigy-menu-quantity-` + id + `" >
            
            ` + quantity + `
             <div>
                <div class="row center">
                    <button onclick="update_quantity(` + id + "," + true + "," + quantity + `)" id="quantity-plus-button" class="badge badge-success"> 
                        <i class="fas fa-plus"></i>
                    </button>
                        &nbsp;&nbsp;
                    <button onclick="update_quantity(` + id + "," + false + "," + quantity + `)" id="quantity-plus-button" class="badge badge-success"> 
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
              </div>
            
            </td>
            <td id="yosigy-menu-subtotal-price-` + id + `">
                ` + discounted_price * quantity + `
            </td>
            <td><button onclick="delete_yosigy_menu(` + id + `)"  class="btn btn-danger btn-sm"><i class="fas fa-times"></i></button></td>
          </tr>`

    var menu_obj = {
        "yosigy_menu_id": yosigy_menu_id,
        "menu_id": id,
        "discounted_price": discounted_price,
        "quantity": 1
    }

    selected_yosigy_menu[id] = menu_obj
    $('#yosigy-detail-menu-table').prepend(menu_item)
    calc_total_price()


}

function delete_yosigy_menu(id) {
    delete selected_yosigy_menu[id]
    $("#yosigy-menu-" + id).empty()

    if (Object.keys(selected_yosigy_menu).length === 0) {

        $("#yosigy-menu-detail-table").remove()
    }
    calc_total_price()
}

function update_quantity(id, up) {
    if (up) {
        if (selected_yosigy_menu[id].quantity > 100) {
            alert("최대 개수는 100개 입니다.")
        } else {
            selected_yosigy_menu[id].quantity += 1
        }


    } else {
        if (selected_yosigy_menu[id].quantity < 2) {
            alert("최소 개수는 1개 입니다.")
        } else {
            selected_yosigy_menu[id].quantity -= 1
        }
    }
    var quantity = selected_yosigy_menu[id].quantity
    $("#yosigy-menu-quantity-" + id).empty()
    $("#yosigy-menu-quantity-" + id).append(
        `` + quantity + `
                <div>
                <div class="row center">
                    <button onclick="update_quantity(` + id + "," + true + "," + quantity + `)" id="quantity-plus-button" class="badge badge-success"> 
                        <i class="fas fa-plus"></i>
                    </button>
                        &nbsp;&nbsp;
                    <button onclick="update_quantity(` + id + "," + false + "," + quantity + `)" id="quantity-plus-button" class="badge badge-success"> 
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
              </div>`
    )

    var subtotal_price = selected_yosigy_menu[id].discounted_price * selected_yosigy_menu[id].quantity
    $("#yosigy-menu-subtotal-price-" + id).empty()
    $("#yosigy-menu-subtotal-price-" + id).append(
        subtotal_price
    )
    calc_total_price()

}

calc_total_price = () => {
    let sum = 0
    Object.values(selected_yosigy_menu).map((value, index,) => {
        sum += value.discounted_price * value.quantity
    })

    $("#yosigy-menu-total-price").empty()
    $("#yosigy-menu-total-price").append(
        `<span class="badge badge-dark"><h4>총 가격: ` + sum + `</h4></span>`
    )
}

