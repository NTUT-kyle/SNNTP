function BackToIndex() {
    document.location.href = "/";
}

function ajax_func(send_url, send_method, data_obj, success_func, error_func) {
    $.ajax({
        url: send_url,
        type: send_method,
        contentType: 'application/json',
        data: JSON.stringify(data_obj),
        success: function(data) {
            return success_func(data);
        },
        error: function(xhr, textStatus, errorThrown) {
            return error_func(xhr, textStatus, errorThrown);
        }
    });
}
