function get_available_yosigy_restaurants(api_url){
    $.ajax({
        type: 'GET',
        url: api_url,
        dataType: 'json',
        error: function (data) {
            if (data.status == 404) {
                $('#menu_select').empty()
            }
        },
        success: function (data) {
            var restaurants = data.restaurants;

            var restaurant_options ='<option value="0">----</option>';
            restaurants.forEach(function (restaurant) {
                restaurant_options += `<option value="`+restaurant.id+`">`+restaurant.title+`</option>`;
            });
            $('#restaurant_select').append(restaurant_options);

            $('#restaurant_select').change(function(){
                var select_value = this.value;
                set_menu_options(api_url+select_value+'/');

                var menu_select_list =
                    `<label for="exampleSelect1">
                        <h4 class="m-2">선택한 메뉴 리스트</h4>
                    </label>
                    <table class="table table-hover">
                        <tr>
                            <thead class="thead-light">
                                <th scope="col">메뉴 이름</th>
                                <th scope="col">메뉴 가격</th>
                                <th scope="col">할인 가격</th>
                                <th scope="col"></th>
                             </thead>
                        </tr>
                        <tbody id="menu_list_data"></tbody>
                    </table>
                    `;
                $('#menu_list').empty();
                $('#menu_list').html(menu_select_list);
            });
        }
    });
}
var menu_dict = {};
var selected_menu_dict = {};

function set_menu_options(api_url){
    $.ajax({
        type: 'GET',
        url: api_url,
        dataType: 'json',
        error: function (data) {
            if (data.status == 404) {
                $('#menu_select').empty()
            }
        },
        success: function (data) {

            var menus = data.menus;

            $('#menu_select').remove();
            $('#menu_select_div').html('<select class="form-control form-control-lg" id="menu_select"></select>');

            var menu_options ='<option value="0">----</option>';

            menu_dict = {};
            selected_menu_dict = {};
            menus.forEach(function (menu) {
                menu_options += `<option value="`+menu.id+`">`+menu.name+`(`+menu.price+`원)</option>`;
                menu_dict[menu.id] = menu;
            });

            $('#menu_select').html(menu_options);

            $('#menu_select').change(function(){
                var select_value = this.value;
                add_menu_list(select_value);
            });
        }
    });
}

function add_menu_list(menu_id){
    if(menu_id==0){
    }else if(!(menu_id in selected_menu_dict)){
        var menu_data = menu_dict[menu_id];
        selected_menu_dict[menu_id] = menu_data;
        var menu_item =
            `<tr id="`+menu_data.id+`">
                <td scope="col">`+menu_data.name+`</td>
                <td scope="col">`+menu_data.price+`원</td>
                <td scope="col">
                    <input type="number" min="0" id="price`+menu_id+`" 
                    step="100" value="`+menu_data.price+`" max="`+menu_data.price+`">원
                </td>
                <th scope="col">
                    <button type="button" class="btn btn-danger btn-sm" 
                    onclick="remove_menu_item(`+menu_data.id+`)">
                        <i class="fas fa-times"></i>
                    </button>
                </th>
            </tr>`;

        $('#menu_list_data').append(menu_item)

    }else {
        alert('이미 추가된 메뉴 입니다.')
    }
}

function create_yosigy_event(api_url){
    var csrftoken = getCookie('csrftoken');
    var form_obj = $('#yosigy_create_form').serializeObject();
    form_obj['menus'] = set_menu_data_to_list();
    var form_data = JSON.stringify(form_obj);

    $.ajax({
        type: 'POST',
        url: api_url,
        data: form_data,
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        error: function (data) {
            var error = data.responseJSON.error;

            if(error.restaurant!=undefined){
                alert(error.restaurant);
                location.reload();
                return false;
            }

            if(typeof error=='string'){
                alert(error);
            }else {
                alert(data.responseJSON.message);
                $('#'+Object.keys(error)+'').focus();
            }

        },
        success: function (data) {
            alert(data.message);
            var yosigy_id = data.yosigy_id;
            location.href='/yosigy/'+yosigy_id

        }
    });
}

function remove_menu_item(menu_id){
    delete selected_menu_dict[menu_id];
    $('#'+menu_id+'').remove();
}

function set_menu_data_to_list(){
    menus = [];
    for(var menu_id in selected_menu_dict) {
        var menu = {
            'id': menu_id,
            'discounted_price': $('#price'+menu_id).val()
        };
        menus.push(menu)
    }
    return menus
}
