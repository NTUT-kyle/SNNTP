function BackToIndex() {
    document.location.href = "/";
}

/*

    Project Not Exist

*/

let SelectType = "";
let Select_Now = "";

function CreateProject() {
    if ($('ProjectExists').length) {
        Select_Now = '#ProjectExists';
    } else {
        $("#ProjectNotExist").hide();
        Select_Now = '#ProjectNotExist';
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

    $.ajax({
        url: "project/" + $("#TypeInput").val(),
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify({
            Type: SelectType
        }),
        success: function(data) {
            console.log(data);
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log('[Error ' + xhr.status + ']: ' + textStatus);
            console.log(errorThrown);
        }
    });

    $("#TypeInput").val('')

    $("#TypeBoard").hide();
    $("#ProjectNotExist").fadeIn(250);
    alert("新增 Project 成功");
    document.location.href = "/";
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
    $('.MenuClick').css('display', 'none');
    Select_Now = '#' + project_name + ' .ProjectExistItem_Top .ProjectExistItem_Menu_Area,#' + project_name + ' .ProjectExistItem_Top .MenuClick';
    $(Select_Now).css('display', 'flex');
    setTimeout(() => {
        Select_Now = '#' + project_name + ' .ProjectExistItem_Top .MenuClick';
    }, 100);
}

// Menu Delect
function ModelDelete(project_name) {
    alert(project_name + ' delete');
}

// Menu Delect
function ModelRename(project_name) {
    alert(project_name + ' rename');
}

// Clicking on all elements except Select_Now makes Select_Now disappear
$(document).on("click", function(event) {
    if (Select_Now == "") return;
    if (!$(event.target).closest(Select_Now).length) {
        $(Select_Now).css('display', 'none');
    }
});
