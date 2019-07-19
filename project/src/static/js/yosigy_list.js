var firstPage = 1;
var tabValue;
var categoryAllId = 3;
var categoryId;

(function(){
    $.ajax({
        type: "GET",
        url: "/api/yosigy/list/"+categoryAllId+"/page/"+firstPage+"/",
        success: yosigyListSuccess,
        error: yosigyListError,
        data: {
            "tab_value": "all",
        }
    });
    $.ajax({
        type: "GET",
        url: "/api/category/",
        success: categoryList,
        dataType: "json",
    });
}());

function categoryList(data) {
    var category = JSON.parse(JSON.stringify(data.category_list));
    var categoryList = '';
    var i;
    category.sort(function (a, b) {
        return a.pk > b.pk ? 1 : a.pk < b.pk ? -1 : 0
    });

    for (i = 0; i < category.length; i++) {
        if (category[i].pk !== 15) {
            categoryList +=
                `<button class="btn btn-outline-primary category-btn" data-category-id="` + category[i].pk + `" style="margin:10px;">` +
                category[i].name +
                `</button>`
        }
    }
    $('#category-lists').html(categoryList);
}

function yosigyListSuccess(data) {
    var html = '';
    if (data['message']) {
        html +=
        `<div class="alert alert-danger" role="alert">` +
            data['message'] +
        `</div>`;
    } else {
        yosigyLists = data['yosigy_list'];
        pageRange = data['page_range'];
        currentPage = data['current_page'];

        for (var i = 0; i < yosigyLists.length; i++) {
            if (yosigyLists[i].is_set_menu_count === undefined){
                yosigyLists[i].is_set_menu_count = 0;
            }
            var isYosigyCount = yosigyLists[i].is_yosigy_count - yosigyLists[i].is_set_menu_count;
            html +=
                `<div class="card col-sm-5 padding-zero m-3">
                <div class="card-footer">
                    <div class="row align-items-center justify-content-left">
                        <div class="m-1">
                            <img src="/media/` + yosigyLists[i].restaurant_img + `"
                                alt="` + yosigyLists[i].restaurant_title + `" width=40px height=40px>
                        </div>
                        <div class="m-1">
                            <h5 class="timeline-title" id="">` + yosigyLists[i].restaurant_title + `</h5>
                        </div>
                    </div>
                </div>
                <div class="card-body text-center">
                    <p class="card-text">` + yosigyLists[i].yosigy_notice + `</p>
                </div>
                <div class="card-footer col-sm text-center">
                    <div class="text-center">
                        <div>
                            <span class="badge badge-danger mr-2">
                                할인메뉴 수
                                <h5>` + isYosigyCount + `</h5>
                            </span>
                            <span class="badge badge-dark ml-2">
                                할인세트 수`;
                                if(yosigyLists[i].is_set_menu_count){
                                    html += `<h5>` + yosigyLists[i].is_set_menu_count + `</h5>`;
                                }else{
                                    html += `<h5>0</h5>`;
                                }
                            html +=
                            `</span>
                            <span class="badge badge-dark ml-2">
                                행사마감기한
                                <h5>` + yosigyLists[i].yosigy_deadline + `</h5>
                            </span>
                        </div>
                    </div>
                    <hr>
                    <button class="btn btn-primary btn-block" onclick="location.href='/yosigy/` + yosigyLists[i].pk + `/'">요식이 티켓 구매</button>
                </div>
            </div>`;
        }
        paginator(pageRange, currentPage);
    }
    if(data['deadline']) {
        $('#deadline-list').html(html);
    }else if(data['all']) {
        $('#yosigy-list').html(html);
    }else{
        $('#yosigy-list').html(html);
        $('#deadline-list').html(html);
    }
}

$(document).on('click', '.category-btn', function(){
    categoryId = $(this)[0].dataset.categoryId;
    tabValue = $(".active").data("tab");
    $.ajax({
        type: "GET",
        url: "/api/yosigy/list/" + categoryId + "/page/"+firstPage+"/",
        success: yosigyListSuccess,
        error: yosigyListError,
        dataType: "json",
        data: {
            "tab_value": tabValue,
        }
    });
});

$(document).on('click', '.nav-link', function(){
    tabValue = $(this)[0].dataset.tab;
    $.ajax({
        type: "GET",
        url: "/api/yosigy/list/"+categoryAllId+"/page/"+firstPage+"/",
        success: yosigyListSuccess,
        error: yosigyListError,
        data: {
            "tab_value": tabValue,
        }
    });
});

$(document).on('click', '.paginator-btn', function(){
   categoryId = $(this)[0].dataset.category;
   var currentPage = $(this)[0].dataset.page;
   $.ajax({
       type: "GET",
       url: "/api/yosigy/list/"+categoryId+"/page/"+currentPage+"/",
       success: yosigyListSuccess,
       error: yosigyListError,
       data: {
            "tab_value": tabValue,
       }
   })
});

function paginator(pageRange, currentPage){
    var paginator = '';
    if(categoryId === undefined){
        categoryId = categoryAllId;
    }
    if(currentPage.has_previous){
        paginator +=
        `<button class="btn btn-outline-primary paginator-btn" data-category="`+categoryId+`" data-page="`+firstPage+`">맨처음</button>
        <button class="btn btn-outline-primary paginator-btn" data-category="`+categoryId+`" data-page="`+currentPage.previous_page_number+`">이전</button> `;
    }
    for(var j = pageRange[0]; j <= pageRange[1]; j++){
        paginator +=
        `<button class="btn btn-outline-primary paginator-btn" data-category="`+categoryId+`" data-page="`+j+`">`+j+`</button> `
    }
    if(currentPage.has_next){
        paginator +=
        `<button class="btn btn-outline-primary paginator-btn" data-category="`+categoryId+`" data-page="`+currentPage.next_page_number+`">다음</button>
        <button class="btn btn-outline-primary paginator-btn" data-category="`+categoryId+`" data-page="`+pageRange[1]+`">맨끝</button>`;
    }
    $('#paginator').html(paginator);
}

function yosigyListError(data){

}
