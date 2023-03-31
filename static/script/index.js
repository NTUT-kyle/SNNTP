function BackToIndex() {
    document.location.href="/";
}

let SelectType = "";
function CreateProject() {
    $("#ProjectNotExist").hide();
    $("#SelectModelType").fadeIn(250);
    $('#SelectModelType').css('display', 'flex');
}

function SelectModel(type) {
    SelectType = type;
    $("#SelectModelType").hide();
    $("#TypeBoard").fadeIn(250);
    $('#TypeBoard').css('display', 'flex');
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
}