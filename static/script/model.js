let projectName = $(".MyProject").html();

/* 

    Center Board Function

*/

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

/* 

    Drag and drop 

*/
let who_are_drag = "";
$("#Test-1, #Test-2, #Test-3").draggable({
    start: (event, ui) => {
        who_are_drag = $(event.target).html();
    },
    revert: "invalid",
    helper: "clone",
    iframeFix: true,
    cursor: "move"
});

let selectItem = null;
$(".modelshow").droppable({
    drop: function( event, ui ) {
        if (who_are_drag == "") return 
        var targetClass = $(`#${who_are_drag}`).attr('class')
        var clone = $(ui.helper).clone().addClass(targetClass);
        clone.click((event) => {
            if (selectItem != null) {
                $(selectItem).css('border', 'unset');
            }
            selectItem = event.target;
            $(selectItem).css('border', '1px solid white');
        });
        clone.draggable({
            containment: ".modelshow",
            scroll: true,
            cursor: "move",
            snap: true
        });
        $(this).append(clone);
        who_are_drag = ""
    }
});

/* 

    Keydown Event 

*/

$(document).keydown(function(event){
    if (event.keyCode == 46) { // del
        if (selectItem != null) {
            $(selectItem).remove();
            selectItem = null;
        }
    }
    // console.log("Key: "+event.keyCode);
});

/* 

    Anywhere Click Event 
    
*/

$(document).on("click", function(event) {
    // Model show item
    if (selectItem != null) {
        if (!$(event.target).closest(selectItem).length) {
            $(selectItem).css('border', 'unset');
            selectItem = null;
        }
    }

    // Center board
    if (!CenterBoard_IsOpen) return;
    let target = '#CenterBoard, #ChooseTrain, #ChooseValidation, #ChooseTest';
    if (!$(event.target).closest(target).length) {
        $('#CenterBoard').css('display', 'none');
        OpenCloseCenterBoard(false, "");
    }
});
