function BackToIndex() {
    document.location.href = "/";
}

let isError = false;
function error_index(xhr, textStatus, errorThrown) {
    console.log("[Error " + xhr.status + "]: " + textStatus);
    console.log(errorThrown);
    isError = true;
}

/*

    Project Not Exist

*/

let SelectType = "";
let Select_Now = "";

function CreateProject() {
    if ($("ProjectExists").length == 0) {
        $("#ProjectNotExist").hide();
    }

    $("#SelectModelType").fadeIn(250);
    $("#SelectModelType").css("display", "flex");
    setTimeout(() => {
        Select_Now = "#SelectModelType";
    }, 100);
}

function SelectModel(type) {
    SelectType = type;
    Select_Now = "#SelectModelType";
    $("#SelectModelType").hide();
    $("#TypeBoard").fadeIn(250);
    $("#TypeBoard").css("display", "flex");
    setTimeout(() => {
        Select_Now = "#TypeBoard";
    }, 100);
}

function TypeOKFromBoard() {
    // alert("Select: " + SelectType + "\nName: " + $("#TypeInput").val())
    if ($("#TypeInput").val() == "") {
        alert();
        $("#msgbox").html("[Error]: 輸入值不能是空的");
        $("#msgbox").css("background-color", "red");
        $("#msgbox").toggle("blind");
        setTimeout(() => {
            $("#msgbox").toggle("blind");
        }, 1500);
        return;
    }
    ajax_func(
        "project/" + $("#TypeInput").val(),
        "POST",
        { Type: SelectType },
        (data) => {
            console.log(data);
            $("#msgbox").html(`成功建立 ${data} Project`);
            $("#msgbox").css("background-color", "#46ffac");
            $("#msgbox").toggle("blind");
            setTimeout(() => {
                $("#msgbox").toggle("blind");
                document.location.href = "/";
            }, 1500);
        },
        error_index,
        () => {
            if (isError) {
                $("#msgbox").html("[Error]: 建立 Project 錯誤!!!");
                $("#msgbox").css("background-color", "red");
                $("#msgbox").toggle("blind");
                setTimeout(() => {
                    $("#msgbox").toggle("blind");
                }, 1500);
                isError = false;
            }
        }
    );
}

/*

    Project Exist

*/

// Into Project
function ModelItem(project_name) {
    ajax_func(
        "/project/" + project_name + "/model/check",
        "GET",
        {},
        (data) => {
            console.log(data);
            if (data == "Success") {
                document.location.href = "/project/" + project_name + "/model";
            } else {
                $("#msgbox").html("[Error]: Project 不存在!!!");
                $("#msgbox").css("background-color", "red");
                $("#msgbox").toggle("blind");
                setTimeout(() => {
                    $("#msgbox").toggle("blind");
                }, 1500);
            }
        },
        error_index,
        () => {
            if (isError) {
                isError = false;
            }
        }
    );
}

// Menu Select
function Item_Menu(project_name) {
    $(Select_Now).css("display", "none");
    $(".MenuClick").css("display", "none");
    Select_Now =
        "#" +
        project_name +
        " .ProjectExistItem_Top .ProjectExistItem_Menu_Area,#" +
        project_name +
        " .ProjectExistItem_Top .MenuClick";
    $(Select_Now).css("display", "flex");
    setTimeout(() => {
        Select_Now = "#" + project_name + " .ProjectExistItem_Top .MenuClick";
    }, 100);
}

// Menu Delete
let deleteProjectName = "";
function ModelDelete(project_name) {
    $("#DeleteBoard").fadeIn(250);
    $("#DeleteBoard").css("display", "flex");
    setTimeout(() => {
        Select_Now = "#DeleteBoard";
    }, 100);
    $("#deleteProjectName").html(project_name);
    deleteProjectName = project_name;
}

function DeleteOKFromBoard() {
    if (deleteProjectName != "") {
        ajax_func(
            "project/" + deleteProjectName,
            "DELETE",
            {},
            (data) => {
                $("#msgbox").html(`成功刪除 ${data} Project`);
                $("#msgbox").css("background-color", "#46ffac");
                $("#msgbox").toggle("blind");
                setTimeout(() => {
                    $("#msgbox").toggle("blind");
                    document.location.href = "/";
                }, 1500);
            },
            error_index,
            () => {
                if (isError) {
                    $("#msgbox").html("[Error]: 刪除 Project 錯誤!!!");
                    $("#msgbox").css("background-color", "red");
                    $("#msgbox").toggle("blind");
                    setTimeout(() => {
                        $("#msgbox").toggle("blind");
                    }, 1500);
                    isError = false;
                }
            }
        );
    }
}

// Menu Rename
let IsModelRename = false;
function ModelRename(project_name) {
    $("#TypeBoard").fadeIn(250);
    $("#TypeBoard").css("display", "flex");
    setTimeout(() => {
        Select_Now = "#TypeBoard";
        IsModelRename = true;
        $("#" + project_name + " .ProjectExistItem_Top .MenuClick").css(
            "display",
            "none"
        );
    }, 100);
    $("#TypeBoard .TypeOK").attr(
        "onclick",
        `ModelRenameSend('${project_name}')`
    );
}

function ModelRenameSend(project_name) {
    if ($("#TypeInput").val() == "") {
        alert("輸入值不能是空的");
        return;
    }
    ajax_func(
        "project/" + project_name,
        "PUT",
        { Rename: $("#TypeInput").val() },
        (data) => {
            $("#msgbox").html(`${data}`);
            $("#msgbox").css("background-color", "#46ffac");
            $("#msgbox").toggle("blind");
            setTimeout(() => {
                $("#msgbox").toggle("blind");
                document.location.href = "/";
            }, 1500);
        },
        error_index,
        () => {
            if (isError) {
                $("#msgbox").html("[Error]: 已有相同名稱的 Project!!!");
                $("#msgbox").css("background-color", "red");
                $("#msgbox").toggle("blind");
                setTimeout(() => {
                    $("#msgbox").toggle("blind");
                }, 1500);
                isError = false;
            }
        }
    );
}

// Clicking on all elements except Select_Now makes Select_Now disappear
$(document).on("click", function (event) {
    if (Select_Now == "") return;
    if (!$(event.target).closest(Select_Now).length) {
        $(Select_Now).css("display", "none");

        if (IsModelRename) {
            $("#TypeBoard .TypeOK").attr("onclick", "TypeOKFromBoard()");
            IsModelRename = false;
        }
        Select_Now = "";
        deleteProjectName = "";
    }
});
