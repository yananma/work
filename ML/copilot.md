

### 05.02

[['没有添加肉粉', [[225, 307], [492, 307], [492, 347], [225, 347]]], ['醇粹黑标系列', [[123, 417], [324, 415], [324, 445], [123, 448]]]]

[['0%谷物', [[127, 469], [205, 469], [205, 487], [127, 487]]], ['85%肉含量', [[127, 496], [234, 496], [234, 513], [127, 513]]], ['使用鲜鱼原料', [[127, 525], [251, 525], [251, 543], [127, 543]]], ['添加鸡肉冻干', [[131, 553], [251, 553], [251, 572], [131, 572]]], ['3', [[250, 741], [267, 741], [267, 759], [250, 759]]]]

[['royalcanin', '[144, 479, 279, 522]'], ['metz', '[544, 568, 658, 606]'], ['metz', '[544, 568, 658, 606]'], ['rose', '[544, 568, 658, 606]'], ['Apple', '[544, 568, 658, 606]']]  

[['英国短毛猫', '[465, 409, 592, 503]'], ['英国长毛猫', '[465, 409, 592, 503]'], ['英国中毛猫', '[465, 409, 592, 503]']]

$(function () {
    get_detail_ajax()
    get_detail_logo_ajax()
    get_detail_breed_ajax()
})

function get_detail_ajax(search_word = '', ocr_select = '有无OCR', logo_select = 'LOGO', breed_select = '品种') {
    $.ajax({
        type: "GET",
        url: get_detail_url_query_string(search_word, ocr_select, logo_select, breed_select),
        async: false,
        success: function (res) {
            show_detail_img(res)
        },
        error: function (e) {
            console.log(e)
        }
    })
    init_load()
}


function detail_right_area_icon_click_function() {

    // 字幕花字 button
    $(document).off("click", ".ocr-small-button").on("click", ".ocr-small-button", function () {
        if ($(this).hasClass("inactive-button") && $(this).text()==="字幕") {
            $(this).removeClass("inactive-button").addClass("active-zimu-button")
            $(this).siblings(".ocr-small-button").removeClass("active-huazi-button").addClass("inactive-button")
        } else if ($(this).hasClass("inactive-button") && $(this).text()==="花字") {
            $(this).removeClass("inactive-button").addClass("active-huazi-button")
            $(this).siblings(".ocr-small-button").removeClass("active-zimu-button").addClass("inactive-button")
        }
        detail_save($(this).parent().find("p"))
    })

    // 删除
    $(document).on("click", ".detail-delete-icon", function () {
        let this_p = $(this).parent().find("p").clone()
        $(this).parent().remove()
        detail_save(this_p)
    })

    // 上移
    $(document).off("click", ".detail-arrow-up-icon").on("click", ".detail-arrow-up-icon", function () {
        let this_line_input = $(this).parent()
        let prev_line = this_line_input.prev()
        if (prev_line.html() !== undefined) {
            prev_line.fadeOut("fast", function () {
                $(this).before(this_line_input)
            }).fadeIn()
        }
        detail_save($(this).parent().find("p"))
    })

    // 下移
    $(document).off("click", ".detail-arrow-down-icon").on("click", ".detail-arrow-down-icon", function () {
        let this_line_input = $(this).parent()
        let next_line = this_line_input.next()
        if (next_line.html() !== undefined) {
            next_line.fadeOut("fast", function () {
                $(this).after(this_line_input)
            }).fadeIn()
        }
        detail_save($(this).parent().find("p"))
    })

    // ocr 右边小 icon
    $(document).off("click", ".ocr-small-plus-icon").on("click", ".ocr-small-plus-icon", function () {
        let one_line_input = $(this).parent().clone();
        one_line_input.find('p').empty().attr('data-position', "");
        $(one_line_input).insertAfter($(this).parent())
        detail_save($(this).parent().find("p"))
    })

    // plus icon 点击添加事件
    $(".ocr-plus-icon").click(function () {
        let wrapper = $(this).parent().siblings(".detail-right-input-area")
        let ocr_div = $("<div />", {class: "one-line-input"})
        ocr_div.append($("<p />", {
            "class": "form-control multi-line-input active-zimu-p",
            "contenteditable": true,
            text: '',
            "data-position": ''
        }))
        ocr_div.append($('<button />', {class: "ocr-small-button active-zimu-button", text: "字幕"}))
        ocr_div.append('<button class=\"ocr-small-button inactive-button\">花字</button>')
        ocr_div.append(get_icons())
        wrapper.prepend(ocr_div)
        detail_save(wrapper.find("p"))
    })

    $(".logo-plus-icon").click(function () {
        let wrapper = $(this).parent().siblings(".detail-right-input-area")
        let logo_div = $("<div />", {class: "one-line-input"})
        logo_div.append($("<p />", {
            class: "form-control multi-line-input",
            "contenteditable": true,
            text: '',
            "data-position": ''
        }))
        logo_div.append("<img src=\"static/plugins/bootstrap-icons-1.8.1/trash.svg\" alt=\"Bootstrap\" class=\"detail-delete-icon\">")
        wrapper.append(logo_div)
        detail_save(wrapper.find("p"))
    })

    $(".breed-plus-icon").click(function () {
        let wrapper = $(this).parent().siblings(".detail-right-input-area")
        let breed_div = $("<div />", {class: "one-line-input"})
        breed_div.append($("<p />", {
            class: "form-control multi-line-input",
            "contenteditable": true,
            text: '',
            "data-position": '',
        }))
        breed_div.append("<img src=\"static/plugins/bootstrap-icons-1.8.1/trash.svg\" alt=\"Bootstrap\" class=\"detail-delete-icon\">")
        wrapper.append(breed_div)
        detail_save(wrapper.find("p"))
    })

    function detail_save(p_selector) {

        function detail_save_ajax(input_data) {
            $.ajax({
                type: "POST",
                url: "/detail_save",
                data: input_data,
                async: false,
                success: function (res) {
                    get_detail_search_word_and_select_text()
                },
                error: function (e) {
                    console.log(e)
                }
            })
        }

        let this_line_input = $(p_selector)

        function detail_save_button_click_function() {
            let save_button = this_line_input.parent().parent().siblings(".detail-right-button-area").find(".right-second-button")
            save_button.css("background-color", "#3399ff").removeAttr("disabled")
            save_button.off("click").on("click", function () {

                function ocr_process_function(input_line, input_line_text, input_line_position) {
                    if (input_line.siblings(".ocr-small-button").hasClass("active-zimu-button")) {
                        input_lines_arr.push({
                            "text": input_line_text,
                            "position": input_line_position,
                            "type": "zimu"
                        })
                    } else if (input_line.siblings(".ocr-small-button").hasClass("active-huazi-button")) {
                        input_lines_arr.push({
                            "text": input_line_text,
                            "position": input_line_position,
                            "type": "huazi"
                        })
                    }
                }

                function logo_or_breed_process_function(input_line_text, input_line_position) {
                    input_lines_arr.push({
                        "text": input_line_text,
                        "position": input_line_position,
                    })
                }

                function category_process_function(input_line, input_line_text, input_line_position) {
                    if (input_line.siblings().hasClass("ocr-small-button")) {
                        ocr_process_function(input_line, input_line_text, input_line_position);
                    } else {
                        logo_or_breed_process_function(input_line_text, input_line_position);
                    }
                }

                let plus_icon_id_arr = $(this).siblings("img").attr("id").split("-")
                let pid = plus_icon_id_arr.slice(-1)[0]
                let input_category = plus_icon_id_arr.slice(0, 1)[0]
                let input_lines = $(this).parent().siblings(".detail-right-input-area").find("p")
                let input_lines_arr = []
                input_lines.each(function () {
                    let input_line = $(this)
                    let input_line_text = input_line.text().trim()
                    let input_line_position = input_line.attr("data-position")
                    if (input_line_text !== "") {
                        category_process_function(input_line, input_line_text, input_line_position);
                    }
                })

                let input_data = {
                    "pid": pid,
                    "input_category": input_category,
                    "input_lines": JSON.stringify(input_lines_arr)
                }
                detail_save_ajax(input_data);
            })
        }

        if (this_line_input.parent().parent().find("p").text().trim() !== "") {
            detail_save_button_click_function();
        } else if (this_line_input.parent().parent().find("p").text().trim() === "") {
            let save_button = this_line_input.parent().parent().siblings(".detail-right-button-area").find(".right-second-button")
            save_button.css("background-color", "#999999").attr("disabled", "disabled")
        }
    }

    $(document).off("input", ".multi-line-input").on("input", ".multi-line-input", function () {
        detail_save(this);
    })
}


function show_detail_img(res) {
    let img_area = $("#detail-img-area")
    img_area.empty()
    for (let i = 0; i < res.data.length; i++) {
        let sql_id = res.data[i]["id"]
        let one_img_row = "<div class=\"one-img-row\">\n" +
            "                <div class=\"img-area-left\">\n" +

            "                    <div class=\"img-area-left-upper-wrapper\" id=\"detail-left-image-area-" + sql_id + "\">\n" +
            "                    </div>\n" +

            "                    <div class=\"img-area-left-lower-wrapper\" id=\"detail-left-image-title-area-" + sql_id + "\">\n" +
            "                    </div>\n" +

            "                </div>\n" +
            "                <div class=\"img-area-right\">\n" +
            "                    <div class=\"button-rows-wrapper\">\n" +
            "                        <div class=\"one-button-row-wrapper\">\n" +
            "                            <div class=\"detail-right-button-area\">\n" +
            "                                <label class=\"right-button-label\">\n" +
            "                                    <img src=\"static/plugins/bootstrap-icons-1.8.1/chevron-down.svg\" alt=\"Bootstrap\" class=\"detail-chevron-icon chevron-down\">\n" +
            "                                </label>\n" +
            "                                <button class=\"right-button detail-ocr-button\" style=\"cursor: default\">OCR</button>\n" +
            "                                <button class=\"right-second-button detail-ocr-save-button\" disabled=\"disabled\">保存</button>\n" +
            "                                <img src=\"static/plugins/bootstrap-icons-1.8.1/plus.png\" alt=\"Bootstrap\" class=\"plus-icon ocr-plus-icon\" id=\"ocr-plus-icon-" + sql_id + "\">\n" +
            "                            </div>\n" +

            "                            <div class=\"detail-right-input-area\" id=\"detail-right-ocr-area-" + sql_id + "\">\n" +
            "                            </div>\n" +
            "                        </div>\n" +
            "\n" +
            "                        <div class=\"one-button-row-wrapper\">\n" +
            "                            <div class=\"detail-right-button-area\">\n" +
            "                                <label class=\"right-button-label\">\n" +
            "                                    <img src=\"static/plugins/bootstrap-icons-1.8.1/chevron-down.svg\" alt=\"Bootstrap\" class=\"detail-chevron-icon chevron-down\">\n" +
            "                                </label>\n" +
            "                                <button class=\"right-button detail-logo-button\" style=\"cursor: default\">LOGO</button>\n" +
            "                                <button class=\"right-second-button detail-logo-save-button\" disabled=\"disabled\">保存</button>\n" +
            "                                <img src=\"static/plugins/bootstrap-icons-1.8.1/plus.png\" alt=\"Bootstrap\" class=\"plus-icon logo-plus-icon\" id=\"logo-plus-icon-" + sql_id + "\">\n" +
            "                            </div>\n" +

            "                            <div class=\"detail-right-input-area\" id=\"detail-right-logo-area-" + sql_id + "\">\n" +
            "                            </div>\n" +

            "                        </div>\n" +
            "\n" +
            "                        <div class=\"one-button-row-wrapper\">\n" +
            "                            <div class=\"detail-right-button-area\">\n" +
            "                                <label class=\"right-button-label\">\n" +
            "                                    <img src=\"static/plugins/bootstrap-icons-1.8.1/chevron-down.svg\" alt=\"Bootstrap\" class=\"detail-chevron-icon chevron-down\">\n" +
            "                                </label>\n" +
            "                                <button class=\"right-button detail-breed-button\" style=\"cursor: default\">品种</button>\n" +
            "                                <button class=\"right-second-button detail-breed-save-button\" disabled=\"disabled\">保存</button>\n" +
            "                                <img src=\"static/plugins/bootstrap-icons-1.8.1/plus.png\" alt=\"Bootstrap\" class=\"plus-icon breed-plus-icon\" id=\"breed-plus-icon-" + sql_id + "\">\n" +
            "                            </div>\n" +

            "                            <div class=\"detail-right-input-area\" id=\"detail-right-breed-area-" + sql_id + "\">\n" +
            "                            </div>\n" +

            "                        </div>\n" +
            "                    </div>\n" +
            "                </div>\n" +
            "            </div>"
        img_area.append(one_img_row)
        detail_left_image_area_func(res, i)
        detail_left_image_title_area_func(res, i)
        detail_right_ocr_area_func(res, i)
        detail_right_flower_subtitles_area_func(res, i)
        detail_right_logo_area_func(res, i)
        detail_right_breed_area_func(res, i)
    }
}


function get_detail_url_query_string(search_word, ocr_select, logo_select, breed_select) {
    if (search_word !== '') {
        return "/true_detail?" + "vid=" + localStorage.getItem('video_id') + "&search_word=" + search_word + "&ocr_select=" + ocr_select + "&logo_select=" + logo_select + "&breed_select=" + breed_select
    } else {
        return "/true_detail?" + "vid=" + localStorage.getItem('video_id') + "&ocr_select=" + ocr_select + "&logo_select=" + logo_select + "&breed_select=" + breed_select
    }
}


// 图片函数
function detail_left_image_area_func(res, i) {
    let sql_id = res.data[i]["id"]
    let image_id = "#detail-left-image-area-" + sql_id
    let image_name = res.data[i]["image_name"]
    let detail_left_image_area = $(image_id)
    detail_left_image_area.append("<input class=\"form-check-input\" type=\"checkbox\" id=\"detail-img-area-checkbox\" value=\"option1\">")
    let img_and_canvas_wrapper = $("<div />", {class: "img-and-canvas-wrapper"}).css({
        width: "832px",
        height: "472px",
        "background-color": "lightgrey"
    })
    let origin_img_height = res.data[i]["img_shape"][0]
    let img = $("<img>", {
        src: "static/" + image_name.split('_')[0] + "/images/" + image_name,
        id: "detail-main-img-" + sql_id,
        "data-origin-img-height": origin_img_height,
        alt: "main-img",
        class: "detail-main-img"
    })
    img_and_canvas_wrapper.append(img)
    detail_left_image_area.append(img_and_canvas_wrapper)
    detail_left_image_area.append("<button class=\"detail-origin-photo-button\">原图</button>")
}


function init_load() {
    let has_loaded = false;

    // 画标注框函数
    function draw_rect(img_and_canvas_wrapper, image) {
        let origin_img_height = parseInt(image.attr("data-origin-img-height"))
        let ratio = image[0].height / origin_img_height
        let ctx = img_and_canvas_wrapper.find("Canvas")[0].getContext("2d")

        function draw_ocr_rect(rect_color) {
            let zimu_position = $(this).attr("data-position").split(",")
            let transformed_position = zimu_position.map(value => Math.round(value * ratio))
            let left_upper = [transformed_position[0], transformed_position[1]]
            let right_upper = [transformed_position[2], transformed_position[3]]
            let right_bottom = [transformed_position[4], transformed_position[5]]
            let left_bottom = [transformed_position[6], transformed_position[7]]
            let x_min = Math.min(left_upper[0], left_bottom[0])
            let y_min = Math.min(left_upper[1], right_upper[1])
            let width = Math.max(right_bottom[0] - left_upper[0], right_upper[0] - left_bottom[0])
            let height = Math.max(left_bottom[1] - right_upper[1], right_bottom[1] - left_upper[1])
            ctx.strokeStyle = rect_color
            ctx.strokeRect(x_min, y_min, width, height)
        }

        function draw_logo_or_breed_rect(position_attr, rect_color) {
            let position = JSON.parse($(this).attr(position_attr))
            let transformed_position = position.map(value => Math.round(value * ratio))
            let x_min = transformed_position[0]
            let y_min = transformed_position[1]
            let width = transformed_position[2] - transformed_position[0]
            let height = transformed_position[3] - transformed_position[1]
            ctx.strokeStyle = rect_color
            ctx.strokeRect(x_min, y_min, width, height)
        }

        img_and_canvas_wrapper.parents("div.one-img-row").find(".detail-right-input-area").find("p").each(function () {
            if ($(this)[0].hasAttribute("data-position")) {
                if ($(this).hasClass("active-zimu-p")) {
                    draw_ocr_rect.call(this, "green");
                } else if ($(this).hasClass("active-huazi-p")) {
                    draw_ocr_rect.call(this, "red");
                }
            } else if ($(this)[0].hasAttribute("data-position")) {
                draw_logo_or_breed_rect.call(this, "data-position", "orange");
            } else if ($(this)[0].hasAttribute("data-position")) {
                draw_logo_or_breed_rect.call(this, "data-position", "purple");
            }
        })
    }

    $("img").off("load").on('load', function () {
        let image = $(this)
        if (image.hasClass('detail-main-img') && !has_loaded) {
            $(".img-and-canvas-wrapper").each(function () {
                let img_and_canvas_wrapper = $(this);
                let sql_id = img_and_canvas_wrapper.find("img").attr("id").split("-").slice(-1)
                img_and_canvas_wrapper.append($("<canvas />", {"id": "detail-canvas-" + sql_id}).css({position: "absolute"}).attr({'width': image[0].width, 'height': image[0].height}));
                draw_rect(img_and_canvas_wrapper, image);
            });
            has_loaded = true;
        }
    })
    detail_right_area_icon_click_function();
}


// 图片 title 函数
function detail_left_image_title_area_func(res, i) {
    let image_title_id = "#detail-left-image-title-area-" + res.data[i]["id"]
    let image_name = res.data[i]["image_name"]
    let detail_left_image_title_area = $(image_title_id)
    const image_title = "        <h3 class=\"img-title\">\n" +
        "                            <p>" + image_name + "</p>\n" +
        "                        </h3>\n" +
        "                        <button class=\"detail-one-img-mark-modified-button\">标为已修</button>\n" +
        "                        <button class=\"detail-ignore-one-img-button\">忽略</button>\n"
    detail_left_image_title_area.append(image_title)
}


function add_zimu_input_line(json_ocr_arr, j, detail_right_ocr_area) {
    let ocr_div = $("<div />", {class: "one-line-input"})
    ocr_div.append($("<p />", {
        "class": "form-control multi-line-input active-zimu-p",
        "contenteditable": true,
        "text": json_ocr_arr[j][0],
        "data-position": json_ocr_arr[j][1]
    }))
    ocr_div.append($('<button />', {class: "ocr-small-button active-zimu-button", text: "字幕"}))
    ocr_div.append('<button class=\"ocr-small-button inactive-button\">花字</button>')
    ocr_div.append(get_icons())
    detail_right_ocr_area.append(ocr_div)
}

// 字幕函数
function detail_right_ocr_area_func(res, i) {
    let ocr_id = "#detail-right-ocr-area-" + res.data[i]["id"]
    let res_ocr = res.data[i]["ocr"]
    if (res_ocr !== null) {
        let json_ocr_arr = JSON.parse(res_ocr.replace(/'/g, "\""))
        let detail_right_ocr_area = $(ocr_id)
        for (let j = 0; j < json_ocr_arr.length; j++) {
            add_zimu_input_line(json_ocr_arr, j, detail_right_ocr_area);
        }
    }
}


function add_huazi_input_line(json_flower_subtitles_arr, j, detail_right_flower_subtitles_area) {
    let flower_subtitles_div = $("<div />", {class: "one-line-input"})
    flower_subtitles_div.append($("<p />", {
        "class": "form-control multi-line-input active-huazi-p",
        "contenteditable": true,
        "text": json_flower_subtitles_arr[j][0],
        "data-position": json_flower_subtitles_arr[j][1]
    }))
    flower_subtitles_div.append('<button class=\"ocr-small-button inactive-button\">字幕</button>')
    flower_subtitles_div.append('<button class=\"ocr-small-button active-huazi-button\">花字</button>')
    flower_subtitles_div.append(get_icons())
    detail_right_flower_subtitles_area.append(flower_subtitles_div)
}

// 花字函数
function detail_right_flower_subtitles_area_func(res, i) {
    let flower_subtitles_id = "#detail-right-ocr-area-" + res.data[i]["id"]
    let res_flower_subtitles = res.data[i]["flower_subtitles"]
    if (res_flower_subtitles !== null) {
        let json_flower_subtitles_arr = JSON.parse(res_flower_subtitles.replace(/'/g, "\""))
        let detail_right_flower_subtitles_area = $(flower_subtitles_id)
        for (let j = 0; j < json_flower_subtitles_arr.length; j++) {
            add_huazi_input_line(json_flower_subtitles_arr, j, detail_right_flower_subtitles_area);
        }
    }
}


// logo 函数
function detail_right_logo_area_func(res, i) {
    let res_logo = res.data[i]["logo"]
    if (res_logo !== null) {
        let json_logo_arr = JSON.parse(res_logo.replace(/'/g, "\""))
        let detail_right_logo_area = $("#detail-right-logo-area-" + res.data[i]["id"])
        for (let j = 0; j < json_logo_arr.length; j++) {
            let logo_div = $("<div />", {class: "one-line-input"})
            logo_div.append($("<p />", {
                class: "form-control multi-line-input",
                "contenteditable": true,
                text: json_logo_arr[j][0],
                "data-position": json_logo_arr[j][1]
            }))
            logo_div.append("<img src=\"static/plugins/bootstrap-icons-1.8.1/trash.svg\" alt=\"Bootstrap\" class=\"detail-delete-icon\">")
            detail_right_logo_area.append(logo_div)
        }
    }
}


// breed 函数
function detail_right_breed_area_func(res, i) {
    let res_breed = res.data[i]["breed"]
    if (res_breed !== null) {
        let json_breed_arr = JSON.parse(res_breed.replace(/'/g, "\""))
        let detail_right_breed_area = $("#detail-right-breed-area-" + res.data[i]["id"])
        for (let j = 0; j < json_breed_arr.length; j++) {
            let breed_div = $("<div />", {class: "one-line-input"})
            breed_div.append($("<p />", {
                class: "form-control multi-line-input",
                "contenteditable": true,
                text: json_breed_arr[j][0],
                "data-position": json_breed_arr[j][1]
            }))
            breed_div.append("<img src=\"static/plugins/bootstrap-icons-1.8.1/trash.svg\" alt=\"Bootstrap\" class=\"detail-delete-icon\">")
            detail_right_breed_area.append(breed_div)
        }
    }
}


// ====================================================================================================================


// 搜索和下拉框函数
function get_detail_search_word_and_select_text() {
    let search_word = $("#detail-search").val()
    let ocr_text = $("#detail-ocr-select").children("option:selected").text()
    let logo_text = $("#detail-logo-select").children("option:selected").text()
    let breed_text = $("#detail-breed-select").children("option:selected").text()
    get_detail_ajax(search_word, ocr_text, logo_text, breed_text)
}


// 获取搜索输入框内容
$(function () {

    // 回车搜索
    $("#detail-search").bind("keypress", function (event) {
        if (event.keyCode === 13) {
            $("#detail-search-btn").trigger("click");
        }
    });

    // 搜索点击事件
    $("#detail-search-btn").click(function () {
        get_detail_search_word_and_select_text()
    })

    // 下拉框筛选事件
    $("#detail-ocr-select, #detail-logo-select, #detail-breed-select").change(function () {
        get_detail_search_word_and_select_text()
    })
})


function get_detail_logo_ajax() {
    get_detail_select_ajax("logo", "LOGO")
}


function get_detail_breed_ajax() {
    get_detail_select_ajax("breed", "品种")
}


function get_detail_select_ajax(category, cate_text) {
    $.ajax({
        type: "GET",
        url: "/detail_" + category + "?vid=" + localStorage.getItem('video_id'),
        async: false,
        success: function (res) {
            get_detail_select(res)
        },
        error: function (e) {
            console.log(e)
        }
    })

    // 获取下拉框数据
    function get_detail_select(res) {
        let detail_select = $("#detail-" + category + "-select")
        detail_select.empty()
        detail_select.append($('<option />', {text: cate_text, value: '0'}))
        for (let i = 0; i < res.data.length; i++) {
            let detail_option = $('<option />', {text: res.data[i], value: i + 1})
            detail_select.append(detail_option)
        }
    }
}



function get_icons() {
    return "<img src=\"static/plugins/bootstrap-icons-1.8.1/trash.svg\" alt=\"Bootstrap\" class=\"detail-delete-icon\">\n" +
        "<img src=\"static/plugins/bootstrap-icons-1.8.1/arrow_up.svg\" alt=\"Bootstrap\" class=\"detail-arrow-icon detail-arrow-up-icon\">\n" +
        "<img src=\"static/plugins/bootstrap-icons-1.8.1/arrow_down.svg\" alt=\"Bootstrap\" class=\"detail-arrow-icon detail-arrow-down-icon\">\n" +
        "<img src=\"static/plugins/bootstrap-icons-1.8.1/plus.svg\" alt=\"Bootstrap\" class=\"ocr-small-plus-icon\">\n"
}
