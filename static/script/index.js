function BackToIndex() {
    document.location.href = "/";
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
    $.ajax({
        url: "project/" + $("#TypeInput").val(),
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({
            Type: SelectType
        }),
        success: function(data) {
            alert(`新增 Project : ${$("#TypeInput").val()} 成功`);
            document.location.href = "/";
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log('[Error ' + xhr.status + ']: ' + textStatus);
            console.log(errorThrown);
        }
    });
}

/*

    Project Exist

*/


// Into Project
function ModelItem(project_name) {
    alert(project_name);
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
    $.ajax({
        url: "project/" + project_name,
        type: "DELETE",
        success: function(data) {
            alert('Project : ' + project_name + ' delete Success');
            document.location.href = "/";
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log('[Error ' + xhr.status + ']: ' + textStatus);
            console.log(errorThrown);
        }
    });
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
    $.ajax({
        url: "project/" + project_name,
        type: "PUT",
        contentType: 'application/json',
        data: JSON.stringify({
            Rename: $("#TypeInput").val()
        }),
        success: function(data) {
            console.log(data);
            alert(data);
            document.location.href = "/";
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log('[Error ' + xhr.status + ']: ' + textStatus);
            console.log(errorThrown);
        }
    });
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
