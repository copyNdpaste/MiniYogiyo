function createCartItem(cart_id, menu_id) {
    const csrftoken = getCookie('csrftoken');
    let url = '/api/cart/' + cart_id + '/'

    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify({'cart': cart_id, 'menu': menu_id}),
        dataType: 'json',
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (data) {

            let errorObj = JSON.parse(String(data.responseText))
            if (errorObj.message === "다른 레스토랑의 메뉴는 주문함에 담을 수 없습니다.") {
                let delete_cart = confirm("다른 레스토랑의 메뉴는 주문함에 담을 수 없습니다. 주문함을 삭제하시겠습니까?")
                if (delete_cart) {
                    const url = "api/cart/" + cart_id + "/delete/"
                    deleteAlreadyExistCart(url, menu_id)
                }
            } else {
                alert(errorObj.message)
            }


        },
        success: function (data) {

            let succes_message = data.menu_name + '을 주문표에 추가하였습니다.'
            alert(succes_message);
            $("#order-menu-count").empty();
            $("#order-menu-count").append(`<span class="badge badge-light">` + data.total_quantity + `</span>`);

        }
    });
}

function deleteCartItem(cart_id, menu_id) {
    const csrftoken = getCookie('csrftoken');
    let url = '/api/cart/' + cart_id + '/' + 'menu' + '/' + menu_id + '/delete/'


    var quantity_text = $("#menu-quantity-" + menu_id).text()

    var quantity = Number(quantity_text)

    var menu_price_text = $("#menu-price-" + menu_id).text().slice(2)
    var subtotal = Number(menu_price_text) * quantity

    var before_total_quantity_text = $("#total-quantity").text().slice(8)
    var total_quantity = Number(before_total_quantity_text) - quantity

    var before_total_price_text = $("#total-price").text().slice(8)
    var total_price = Number(before_total_price_text) - subtotal

    $.ajax({
        type: 'DELETE',
        url: url,
        dataType: 'json',
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (request) {
            alert("삭제가 취소 되었습니다.")
        },
        success: function (data) {
            if (data.total_quantity === 0) {
                alert("메뉴가 삭제되었습니다.")
                $("#restaurant-info").empty();
                $("#menu-table").empty();
                $("#cart-info").empty();
                $("#order-menu-count").empty();
                $("#order-menu-count").append(`<span class="badge badge-light">` + total_quantity + `</span>`);
                $("#main").append(
                    `<div style="text-align:center;">
                    <h3>` + '주문표는 현재 비어있습니다.' + `</h3>
                </div>`
                )
            } else {
                alert("메뉴가 삭제되었습니다.")


                $("#menu-row-" + menu_id).remove();
                $("#order-menu-count").empty();
                $("#order-menu-count").append(`<span class="badge badge-light">` + total_quantity + `</span>`);
                var menu_count_update_val = $("#menu-count").val() - 1
                $("#menu-count").val(menu_count_update_val);
                $("#menu-row-" + menu_id).remove();


                $("#total-quantity").empty();
                $("#total-quantity").append(
                    `<p class="total">총 메뉴 수: ` + total_quantity + `</p>`
                );

                $("#total-price").empty();
                $("#total-price").append(
                    `<p class="total">총 가격: ￦ ` + total_price + `</p>`
                );
            }


        }
    });
}

function deleteCart(delete_url) {
    const csrftoken = getCookie('csrftoken');
    let url = delete_url
    alert(url)

    $.ajax({
        type: 'DELETE',
        url: url,
        dataType: 'json',
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (request) {
            console.log(request)
            alert("삭제가 취소 되었습니다.")
        },
        success: function (data) {
            alert("주문표가 삭제되었습니다.")

            $("#restaurant-info").empty();
            $("#menu-table").empty();
            $("#cart-info").empty();
            $("#main").append(
                `<div style="text-align:center;">
                  <h3>` + data.message + `</h3>
              </div>`
            )

        }
    });
}

function deleteAlreadyExistCart(delete_url, menu_id) {
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'DELETE',
        url: "http://127.0.0.1:8000/" + delete_url,
        dataType: 'json',
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (request) {
            console.log(request)
            alert("삭제가 취소 되었습니다.")
        },
        success: function (data) {

            reCreateCartItem(data.cart_id, menu_id)
        }
    });
}

function reCreateCartItem(cart_id, menu_id) {
    const csrftoken = getCookie('csrftoken');
    let url = '/api/cart/' + cart_id + '/'

    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify({'cart': cart_id, 'menu': menu_id}),
        dataType: 'json',
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (data) {
            alert("주문함에 담는 것을 실패하였습니다.")
        },
        success: function (data) {
            alert("기존메뉴가 삭제되고," + data.menu_name + "가 추가되었습니다.")
            $("#order-menu-count").empty();
            $("#order-menu-count").append(`<span class="badge badge-light">` + data.total_quantity + `</span>`);
        }
    });
}

function upQuantity(menu_id) {
    var quantity_text = $("#menu-quantity-" + menu_id).text()

    var quantity = Number(quantity_text) + 1


    if (quantity == 101) {
        alert("최고 수량은 100개 입니다.");
        quantity = 100
    }

    var menu_price_text = $("#menu-price-" + menu_id).text().slice(2)
    var subtotal = Number(menu_price_text) * quantity

    var before_total_quantity_text = $("#total-quantity").text().slice(8)
    var total_quantity = Number(before_total_quantity_text) + 1

    var before_total_price_text = $("#total-price").text().slice(8)
    var total_price = Number(before_total_price_text) + Number(menu_price_text)

    $("#menu-quantity-" + menu_id).empty();
    $("#menu-quantity-" + menu_id).append(
        quantity + `<div>
                        <div class="row center">
                          <button onclick="upQuantity(` + menu_id + `)" class="badge badge-success"> 
                              <i class="fas fa-plus"></i>
                          </button>
                              &nbsp;&nbsp;
                          <button onclick="downQuantity(` + menu_id + `)"  class="badge badge-success"> 
                              <i class="fas fa-minus"></i>
                          </button>
                        </div>
                    </div>`
    )

    $("#menu-subtotal-" + menu_id).empty();
    $("#menu-subtotal-" + menu_id).append(
        `￦ ` + subtotal
    )

    $("#total-quantity").empty();
    $("#total-quantity").append(
        `<p class="total">총 메뉴 수: ` + total_quantity + `</p>`
    );

    $("#total-price").empty();
    $("#total-price").append(
        `<p class="total">총 가격: ￦ ` + total_price + `</p>`
    );
    $("#order-menu-count").empty();
    $("#order-menu-count").append(`<span class="badge badge-light">` + total_quantity + `</span>`);

}

function downQuantity(menu_id) {
    var quantity_text = $("#menu-quantity-" + menu_id).text()
    var quantity = Number(quantity_text) + 1

    var menu_price_text = $("#menu-price-" + menu_id).text().slice(2)
    var subtotal = Number(menu_price_text) * quantity

    var before_total_quantity_text = $("#total-quantity").text().slice(8)
    var total_quantity = Number(before_total_quantity_text) - 1

    var before_total_price_text = $("#total-price").text().slice(8)
    var total_price = Number(before_total_price_text) - Number(menu_price_text)

    if (quantity == 0) {
        alert("최소 수량은 1개 입니다.");
        quantity = 1
        total_quantity = total_quantity + 1
        total_price = total_prie + Number(menu_price_text)
    }

    $("#menu-quantity-" + menu_id).empty();
    $("#menu-quantity-" + menu_id).append(
        quantity + `<div>
                            <div class="row center">
                            <button onclick="upQuantity(` + menu_id + `)" class="badge badge-success"> 
                                <i class="fas fa-plus"></i>
                            </button>
                                &nbsp;&nbsp;
                            <button onclick="downQuantity(` + menu_id + `)"  class="badge badge-success"> 
                                <i class="fas fa-minus"></i>
                            </button>
                            </div>
                          </div>`
    )

    $("#menu-subtotal-" + menu_id).empty();
    $("#menu-subtotal-" + menu_id).append(
        `￦ ` + subtotal
    )

    $("#total-quantity").empty();
    $("#total-quantity").append(
        `<p class="total">총 메뉴 수: ` + total_quantity + `</p>`
    );

    $("#total-price").empty();
    $("#total-price").append(
        `<p class="total">총 가격: ￦ ` + total_price + `</p>`
    );
    $("#order-menu-count").empty();
    $("#order-menu-count").append(`<span class="badge badge-light">` + total_quantity + `</span>`);

}

function updateQuantity(menu_list, cart_id, num) {
    const csrftoken = getCookie('csrftoken');
    let url = '/api/cart/' + cart_id + '/' + 'update/'
    let menu_id_list = decodeURIComponent(menu_list).split(',')

    let menu_obj_list = []
    menu_id_list.map((menu_id) => {
        var quantity_text = $("#menu-quantity-" + menu_id).text()
        var menu_id = $("#menu-" + menu_id).val()

        if (Number(quantity_text) !== 0) {
            menu_obj_list.push({"menu": Number(menu_id), "quantity": Number(quantity_text)})
        }

    })

    $.ajax({
        type: 'PUT',
        url: url,
        data: JSON.stringify(menu_obj_list),
        dataType: 'json',
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (request) {
            if (request.status === 400) {
                console.log("400 에러")
            }
        },
        success: function (data) {
            if (num == 1) {
                alert("주문표가 저장되었습니다.")
            } else {
                window.location.href = 'http://127.0.0.1:8000/order/'

            }

        }
    });
};
