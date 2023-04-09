let projectName = $(".MyProject").html();

// Choose data function

$('#CBFileButton').click(() => {
    $('#CBFile').trigger('click');
});

let formData = new FormData();
$("#CBFile").on("change", function () {
    formData.delete('file');
    formData.append('file', this.files[0]);
});

let uploadStatus = "";
let CenterBoard_IsOpen = false;
$('#ChooseTrain').click(() => {
    OpenCloseCenterBoard(true, "Training");
});
$('#ChooseValidation').click(() => {
    OpenCloseCenterBoard(true, "Validation");
});
$('#ChooseTest').click(() => {
    OpenCloseCenterBoard(true, "Test");
});

function OpenCloseCenterBoard(openOrNot, titleValue) {
    uploadStatus = titleValue;
    $('#CenterBoardText').html(`${titleValue} data path`);
    if(openOrNot) {
        if (CenterBoard_IsOpen) return;
        $('#CenterBoard').fadeIn();
        $('#CenterBoard').css('display', 'flex');
        setTimeout(() => {
            CenterBoard_IsOpen = true;
        }, 300);
    } else {
        CenterBoard_IsOpen = false;
        $('#CenterBoard').fadeOut();
    }
}

function successSendFile(data) {
    alert(data);
}

function error_func(xhr, textStatus, errorThrown) {
    console.log('[Error ' + xhr.status + ']: ' + textStatus);
    console.log(errorThrown);
    alert('error');
}

$("#CenterBoardButton").click(() => {
    if (uploadStatus == "") return
    ajax_func(
        '/model/' + projectName + '/' + uploadStatus,
        'POST',
        formData,
        successSendFile,
        error_func
    );
});

$(document).on("click", function(event) {
    if (!CenterBoard_IsOpen) return;
    let target = '#CenterBoard, #ChooseTrain, #ChooseValidation, #ChooseTest';
    if (!$(event.target).closest(target).length) {
        $('#CenterBoard').css('display', 'none');
        OpenCloseCenterBoard(false, "");
    }
});