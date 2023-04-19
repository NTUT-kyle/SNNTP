let projectName = $(".MyProject").html();

/* 

    Center Board Function

*/

$("#CBFileButton").click(() => {
    $("#CBFile").trigger("click");
});

let formData = new FormData();
$("#CBFile").on("change", function () {
    formData.delete("file");
    formData.append("file", this.files[0]);
});

let uploadStatus = "";
let CenterBoard_IsOpen = false;
$("#ChooseTrain").click(() => {
    OpenCloseCenterBoard(true, "Training");
});
$("#ChooseValidation").click(() => {
    OpenCloseCenterBoard(true, "Validation");
});
$("#ChooseTest").click(() => {
    OpenCloseCenterBoard(true, "Test");
});

function OpenCloseCenterBoard(openOrNot, titleValue) {
    uploadStatus = titleValue;
    $("#CenterBoardText").html(`${titleValue} data path`);
    if (openOrNot) {
        if (CenterBoard_IsOpen) return;
        $("#CenterBoard").fadeIn();
        $("#CenterBoard").css("display", "flex");
        setTimeout(() => {
            CenterBoard_IsOpen = true;
        }, 300);
    } else {
        CenterBoard_IsOpen = false;
        $("#CenterBoard").fadeOut();
    }
}

function successSendFile(data) {
    alert(data);
}

function error_func(xhr, textStatus, errorThrown) {
    console.log("[Error " + xhr.status + "]: " + textStatus);
    console.log(errorThrown);
    alert("error");
}

$("#CenterBoardButton").click(() => {
    if (uploadStatus == "") return;
    ajax_func(
        "/model/" + projectName + "/" + uploadStatus,
        "POST",
        formData,
        successSendFile,
        error_func
    );
});

$(".SelectItem").click(() => {
    graphyPackage();
});

/* 

    Drag and drop 

*/

let mySVG = $("#droparea").connect($("#droparea"), 3, 171);

let who_are_dragging = "";
// Set drag event
$(".layerCategory div div:not(:first-child)").draggable({
    start: (event, ui) => {
        who_are_dragging = $(event.target).html();
    },
    revert: "invalid",
    helper: "clone",
    cursor: "move",
});

let initItemId = 0;
let initPointID = 0; // initPointID for droparea item
let selectItem = null; // select item for del
let dropItemPointDown = []; // record select item point
let connectingLine = []; // record two point vector
let isInputLayerPlace = false;
let isOutputLayerPlace = false;

// Set drop event
$(".droparea").droppable({
    drop: function (event, ui) {
        if (who_are_dragging == "") return;

        // get drop element and set class and id
        var clone = $(ui.helper).clone().addClass("dropItem");
        clone.attr("id", "item_" + initItemId);
        clone.attr("name", who_are_dragging);
        initItemId += 1;

        // set drop element html
        if (who_are_dragging == "Input") {
            if (isInputLayerPlace) {
                alert_func("Cannot place more than two Input Layer", "red");
                return;
            }
            clone.html(`
                <div></div>
                ${clone.html()}
                <div id="p${initPointID}" class="dropItemPoint dropItemPointRight"></div>
            `);
            initPointID += 1;
            isInputLayerPlace = true;
        } else if (who_are_dragging == "Output") {
            if (isOutputLayerPlace) {
                alert_func("Cannot place more than two Output Layer", "red");
                return;
            }
            clone.html(`
                <div id="p${initPointID}" class="dropItemPoint dropItemPointLeft"></div>
                ${clone.html()}
                <div></div>
            `);
            initPointID += 1;
            isOutputLayerPlace = true;
        } else {
            clone.html(`
                <div id="p${initPointID}" class="dropItemPoint dropItemPointLeft"></div>
                ${clone.html()}
                <div id="p${
                    initPointID + 1
                }" class="dropItemPoint dropItemPointRight"></div>
            `);
            initPointID += 2;
        }

        // reset position
        let offset = $(this).offset();
        clone.css("top", `calc(${clone.css("top")} - ${offset.top}px)`);
        clone.css("left", `calc(${clone.css("left")} - ${offset.left}px)`);

        // click event for drop element
        clone.click((event) => {
            // disable border if selectItem exist
            if (selectItem != null) {
                if ($(selectItem).hasClass("dropItem")) {
                    $(selectItem).css("border", "1px solid black");
                } else {
                    $(selectItem).css("border", "unset");
                }
            }

            if ($(event.target).hasClass("dropItemPoint")) {
                // select item point process
                // append to dropItemPointDown
                if (
                    dropItemPointDown.length > 0 &&
                    $(event.target).attr("id") ==
                        dropItemPointDown[0].attr("id")
                ) {
                    $(dropItemPointDown[0]).css("background-color", "unset");
                    dropItemPointDown = [];
                    return;
                }

                dropItemPointDown.push($(event.target));

                // if it select two point, make line
                if (dropItemPointDown.length == 2) {
                    let c1 = getConnectElementIndex(dropItemPointDown[0]);
                    let c2 = getConnectElementIndex(dropItemPointDown[1]);
                    // check if two points is connected?
                    if (c1 != -1 && c1 == c2) {
                        alert_func("Line is connected.", "yellow");
                        $(dropItemPointDown[0]).css(
                            "background-color",
                            "unset"
                        );
                        dropItemPointDown = [];
                        return;
                    }
                    // check if two points parent same
                    if (
                        $(dropItemPointDown[0]).parent().attr("id") ==
                        $(dropItemPointDown[1]).parent().attr("id")
                    ) {
                        alert_func(
                            "Same layer cannot connect together.",
                            "yellow"
                        );
                        $(dropItemPointDown[0]).css(
                            "background-color",
                            "unset"
                        );
                        dropItemPointDown = [];
                        return;
                    }

                    // draw
                    drawOneLine(
                        dropItemPointDown[0],
                        dropItemPointDown[1],
                        "#ff8d8d"
                    );
                    // append vector
                    connectingLine.push([
                        dropItemPointDown[0],
                        dropItemPointDown[1],
                    ]);
                    // clear value
                    $(dropItemPointDown[0]).css("background-color", "unset");
                    $(dropItemPointDown[1]).css("background-color", "unset");
                    dropItemPointDown = [];
                } else {
                    $(event.target).css("background-color", "yellow");
                }
                selectItem = null; // prevent del event
            } else {
                // select item process
                if (dropItemPointDown.length > 0) {
                    // clear value
                    dropItemPointDown[0].css("background-color", "unset");
                    dropItemPointDown = [];
                }
                // set selectItem to target & set target border
                selectItem = event.target;
                $(selectItem).css("border", "1px dashed white");
            }
        });

        // drag event for drop element
        clone.draggable({
            drag: function () {
                if (connectingLine.length) {
                    // if has line connected
                    mySVG.redrawLines();
                }
                // check the element size and scale the parent size
                setDropAreaSize();

                // set scrollbar position
                let offset = $(this).offset();
                // $(".modelshow").scrollTop(offset.top);
                // $(".modelshow").scrollLeft(offset.left);
            },
            cancel: "div.dropItemPoint",
            scroll: true,
            cursor: "move",
            snap: true,
        });

        // add drop element to droparea
        $(this).append(clone);
        who_are_dragging = "";
    },
});

// reset drop area size method
function setDropAreaSize() {
    let maxWidth = 0;
    let maxHeight = 0;

    // find max width and height
    $(".dropItem").each((index, element) => {
        // for width situation
        if (maxWidth <= $(element).position().left + $(element).width()) {
            maxWidth = $(element).position().left + $(element).width() + 2;
        }
        // for height situation
        if (maxHeight <= $(element).position().top + $(element).height()) {
            maxHeight = $(element).position().top + $(element).height() + 2;
        }
    });

    // compare with "modelshow" element
    if ($(".modelshow").width() < maxWidth) {
        $(".droparea").width(maxWidth);
    } else {
        $(".droparea").width($(".modelshow").width());
    }

    if ($(".modelshow").height() < maxHeight) {
        $(".droparea").height(maxHeight);
    } else {
        $(".droparea").height($(".modelshow").height());
    }
}

// draw p1 to p2 of line
function drawOneLine(p1, p2, colorCode) {
    mySVG.drawLine({
        left_node: "#" + $(p1).attr("id"),
        right_node: "#" + $(p2).attr("id"),
        color: colorCode,
        style: "solid",
        horizantal_gap: 10,
        error: true,
        width: 1,
    });
}

// check if element exists
function getConnectElementIndex(point) {
    return connectingLine.findIndex(
        (element) =>
            $(element[0]).attr("id") == $(point).attr("id") ||
            $(element[1]).attr("id") == $(point).attr("id")
    );
}

// get another element from vector
function getAnotherPoint(vector, point) {
    return vector[0] == point ? vector[1] : vector[0];
}

function putSetIntoMap(LayerMap, parent1, parent2, point1_id) {
    if (!LayerMap.has(parent1.attr("id"))) {
        LayerMap.set(parent1.attr("id"), {
            name: parent1.attr("name"),
            posX: parent1.position().left,
            posY: parent1.position().top,
            point_L_con: [],
            point_R_con: [],
        });
    }
    if ($(point1_id).hasClass("dropItemPointLeft")) {
        LayerMap.get(parent1.attr("id")).point_L_con.push(parent2.attr("id"));
    } else {
        LayerMap.get(parent1.attr("id")).point_R_con.push(parent2.attr("id"));
    }
    return LayerMap;
}

function graphyPackage() {
    let LayerMap = new Map();
    connectingLine.forEach((value) => {
        let point_id = value[0];
        let parent = $(point_id).parent();
        let ano_point_id = value[1];
        let ano_parent = $(ano_point_id).parent();

        // set first element value
        LayerMap = putSetIntoMap(LayerMap, parent, ano_parent, point_id);
        // set second element value
        LayerMap = putSetIntoMap(LayerMap, ano_parent, parent, ano_point_id);
    });
    console.log(LayerMap);
}

/*

{
    id: {
        name: STRING
        posX: FLOAT
        posY: FLOAT
        point_L_con: [
            id1, id2
        ],
        point_R_con: [
            id2, id3
        ],
    }
}

*/

// key del method
function del_func() {
    if (selectItem != null) {
        $(selectItem).remove();

        if ($(selectItem).html().indexOf("Input")) {
            isInputLayerPlace = false;
        } else if ($(selectItem).html().indexOf("Output")) {
            isOutputLayerPlace = false;
        }
        selectItem = null;
        setDropAreaSize();
        // redraw canvas
        if (connectingLine.length) {
            // if has line connected
            mySVG.redrawLines();
        }
    }

    if (dropItemPointDown.length > 0) {
        // Check is element connected
        let findIndex = getConnectElementIndex(dropItemPointDown[0]);
        if (findIndex != -1) {
            // If it connected, clear dropItemPointDown list
            dropItemPointDown[0].css("background-color", "unset");
            dropItemPointDown = [];

            // trigger canvas deleteLine
            mySVG.deleteLine({
                left_node: "#" + $(connectingLine[findIndex][0]).attr("id"),
                right_node: "#" + $(connectingLine[findIndex][1]).attr("id"),
            });

            // delete element from List
            connectingLine.splice(findIndex, 1);

            // redraw canvas
            mySVG.redrawLines();
        }
    }
}

/*

    Alert Dialog

*/

function alert_func(msg, color) {
    $("#AlertDialog").css("background-color", color);
    $("#AlertDialog").html(msg);
    $("#AlertDialog").toggle("blind");
    $("#AlertDialog").effect("bounce");
    setTimeout(() => {
        $("#AlertDialog").toggle("blind");
    }, 3000);
}

/*

    Scroll event

*/

$(".modelshow").scroll(() => {
    if (connectingLine.length) {
        mySVG.redrawLines();
    }
});

/*

    Window Resize Event

*/

$(window).on("resize", function () {
    if ($(".modelshow").width() > $(".droparea").width()) {
        $(".droparea").width($(".modelshow").width());
    }
    if ($(".modelshow").height() > $(".droparea").height()) {
        $(".droparea").height($(".modelshow").height());
    }
});

/* 

    Keydown Event 

*/

$(document).keydown(function (event) {
    if (event.keyCode == 46) {
        // del keycode
        del_func();
    }
});

/* 

    Anywhere Click Event 
    
*/

$(document).on("click", function (event) {
    // Model show item
    if (selectItem != null) {
        if (!$(event.target).closest(selectItem).length) {
            $(selectItem).css("border", "1px solid black");
            selectItem = null;
        }
    }

    // drop item of droparea
    if (dropItemPointDown.length > 0) {
        if (
            !(
                $(event.target).closest(dropItemPointDown[0]).length ||
                $(event.target).closest(dropItemPointDown[1]).length
            )
        ) {
            dropItemPointDown.forEach((value) => {
                $(value).css("background-color", "unset");
            });
            dropItemPointDown = [];
        }
    }

    // Center board
    if (!CenterBoard_IsOpen) return;
    let target = "#CenterBoard, #ChooseTrain, #ChooseValidation, #ChooseTest";
    if (!$(event.target).closest(target).length) {
        $("#CenterBoard").css("display", "none");
        OpenCloseCenterBoard(false, "");
    }
});
