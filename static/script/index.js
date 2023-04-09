function BackToIndex() {
    document.location.href = "/";
}

function success_index(data) {
    $('#msgbox').html(data);
    $('#msgbox').css('background-color', '#46ffac');
    $('#msgbox').toggle("blind");
    setTimeout(() => {
        $('#msgbox').toggle("blind");
        document.location.href = "/";
    }, 1500);
}

function error_index(xhr, textStatus, errorThrown) {
    console.log('[Error ' + xhr.status + ']: ' + textStatus);
    console.log(errorThrown);
    $('#msgbox').html('[Error ' + xhr.status + ']: ' + errorThrown);
    $('#msgbox').css('background-color', 'red');
    $('#msgbox').toggle("blind");
    setTimeout(() => {
        $('#msgbox').toggle("blind");
    }, 1500);
}

/*

    Project Not Exist

*/

let SelectType = "";
let Select_Now = "";

function CreateProject() {
    if ($('ProjectExists').length == 0) {
        $("#ProjectNotExist").hide();
    }

    $("#SelectModelType").fadeIn(250);
    $('#SelectModelType').css('display', 'flex');
    setTimeout(() => {
        Select_Now = '#SelectModelType';
    }, 100);
  }

function SelectModel(type) {
    SelectType = type;
    Select_Now = '#SelectModelType';
    $("#SelectModelType").hide();
    $("#TypeBoard").fadeIn(250);
    $('#TypeBoard').css('display', 'flex');
    setTimeout(() => {
        Select_Now = '#TypeBoard';
    }, 100);
}

function TypeOKFromBoard() {
    // alert("Select: " + SelectType + "\nName: " + $("#TypeInput").val())
    if ($("#TypeInput").val() == "") {
        alert("輸入值不能是空的");
        return;
    }
    ajax_func(
        "project/" + $("#TypeInput").val(),
        "POST",
        {Type: SelectType},
        success_index,
        error_index
    );
}

/*

    Project Exist

*/


// Into Project
function ModelItem(project_name) {
    ajax_func(
        '/project/' + project_name + '/model',
        "GET",
        {},
        (data) => { 
            document.location.href = data;
        },
        error_index
    );
}

// Menu Select
function Item_Menu(project_name) {
    $(Select_Now).css('display', 'none');
    $('.MenuClick').css('display', 'none');
    Select_Now = '#' + project_name + ' .ProjectExistItem_Top .ProjectExistItem_Menu_Area,#' + project_name + ' .ProjectExistItem_Top .MenuClick';
    $(Select_Now).css('display', 'flex');
    setTimeout(() => {
        Select_Now = '#' + project_name + ' .ProjectExistItem_Top .MenuClick';
    }, 100);
}

// Menu Delete
function ModelDelete(project_name) {
    ajax_func(
        "project/" + project_name,
        "DELETE",
        {},
        success_index,
        error_index
    );
}

// Menu Rename
let IsModelRename = false;
function ModelRename(project_name) {
    $("#TypeBoard").fadeIn(250);
    $('#TypeBoard').css('display', 'flex');
    setTimeout(() => {
        Select_Now = '#TypeBoard';
        IsModelRename = true;
        $('#' + project_name + ' .ProjectExistItem_Top .MenuClick').css('display', 'none');
    }, 100);
    $('#TypeBoard .TypeOK').attr('onclick', `ModelRenameSend('${project_name}')`)
}

function ModelRenameSend(project_name) {
    if ($("#TypeInput").val() == "") {
        alert("輸入值不能是空的");
        return;
    }
    ajax_func(
        "project/" + project_name,
        "PUT",
        {Rename: $("#TypeInput").val()},
        success_index,
        error_index
    );
}

// Clicking on all elements except Select_Now makes Select_Now disappear
$(document).on("click", function(event) {
    if (Select_Now == "") return;
    if (!$(event.target).closest(Select_Now).length) {
        $(Select_Now).css('display', 'none');

        if (IsModelRename) {
            $('#TypeBoard .TypeOK').attr('onclick', 'TypeOKFromBoard()')
            IsModelRename = false
        }
        Select_Now = ""
    }
});
