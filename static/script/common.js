function BackToIndex() {
    document.location.href = "/";
}

function ajax_func(
    send_url,
    send_method,
    data_obj,
    success_func,
    error_func,
    done_func,
    isFormType = false
) {
    if (isFormType) {
        $.ajax({
            url: send_url,
            type: send_method,
            contentType: false,
            processData: false,
            cache: false,
            data: data_obj,
            mimeType: 'multipart/form-data',
            header: {
                'Content-Type': 'multipart/form-data'
            },
            success: function (data, textStatus) {
                return success_func(data);
            },
            error: function (xhr, textStatus, errorThrown) {
                return error_func(xhr, textStatus, errorThrown);
            },
            complete: function (xhr, textStatus) {
                return done_func();
            },
        });
    } else {
        $.ajax({
            url: send_url,
            type: send_method,
            contentType: "application/json",
            data: JSON.stringify(data_obj),
            success: function (data, textStatus) {
                return success_func(data);
            },
            error: function (xhr, textStatus, errorThrown) {
                return error_func(xhr, textStatus, errorThrown);
            },
            complete: function (xhr, textStatus) {
                return done_func();
            },
        });
    }
}
