let projectName = $(".MyProject").html();
let isErrorHappen = false;

/* 

    Center Board Function

*/

$("#CBFileButton").click(() => {
    $("#CBFile").trigger("click");
});

let formData = new FormData();
$("#CBFile").on("change", function () {
    if($("#CBFile").val() == '') return;
    formData.delete("file");
    formData.append("file", this.files[0]);
    formData.delete("type");
    formData.append("type", uploadStatus);
    let fileName = $("#CBFile").val().split('\\').pop();
    $("#CBFileButton").html(fileName == ''?'選擇檔案':fileName)
});

let uploadStatus = "";
let CenterBoard_IsOpen = false;
$("#ChooseTrain").click(() => {
    OpenCloseCenterBoard(true, "Training");
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
    console.log(data);
}

function error_func(xhr, textStatus, errorThrown) {
    console.log("[Error " + xhr.status + "]: " + textStatus);
    console.log(errorThrown);
    // alert_func(errorThrown, "red", 3000);
    isErrorHappen = true;
}

$("#CenterBoardButton").click(() => {
    if (uploadStatus == "") return;
    if ($("#CBFile").val() == "") {
        alert_func("Choose a zip file to upload!", "yellow", 3000);
        return;
    }
    ajax_func(
        "/model/" + projectName + "/upload",
        "POST",
        formData,
        (data) => {
            alert_func(data, "#0dff00", 3000);
            $("#CenterBoard").css("display", "none");
            OpenCloseCenterBoard(false, "");
            $("#CBFile").val('');
            $("#CBFileButton").html('選擇檔案');
        },
        error_func,
        () => {
            if (isErrorHappen) {
                alert_func("Fail Upload File", "red", 3000);
                isErrorHappen = false;
            }
        },
        true
    );
});

/* 

    Training & Model Function

*/

function Build_Model() {
    ajax_func(
        "/model/" + projectName + "/create",
        "GET",
        {},
        successSendFile,
        error_func,
        () => {
            if (isErrorHappen) {
                alert_func("Fail Build Model", "red", 3000);
                isErrorHappen = false;
            } else {
                alert_func("Success Build Model", "#0dff00", 3000);
                $("#train_model p").html("Train Model");
                TrainingBoardOpenClose(false);
                $("#TrainingSetting").fadeOut();
            }
        }
    );
}

function Create_Model_File() {
    let model_package = {
        model_List: ModelPackage(),
        model_parameter: {
            batch_size: parseInt($("#SettingBatchSize").val()), 
            epochs: parseInt($("#SettingEpoch").val()),
            optimizer: $("#SettingOptimizer").val(),
            loss: $("#SettingLoss").val(),
            validation_split: parseFloat($("#SettingValidationSplit").val()),
        }
    };
    console.log(model_package);
    if (model_package.model_List.length) {
        ajax_func(
            "/model/" + projectName + "/build",
            "POST",
            model_package,
            successSendFile,
            error_func,
            () => {
                if (isErrorHappen) {
                    alert_func("Fail Create Model File", "red", 3000);
                    isErrorHappen = false;
                } else {
                    console.log("Success create model file");
                    Build_Model();
                }
            }
        );
    }
}

let trainingProcessObject;
let isTrainingStart = false;

function trainingProcess() {
    ajax_func(
        "/model/getModelState",
        "GET",
        {},
        (data) => {
            console.log(data);
            if (data.training_state == "init") {
                $("#TrainingStatus").html("Initialization");
            } else if (data.training_state == "training") {
                $("#TrainingStatus").html("Training...");
                $("#TrainingTime").html((data.training_time).toFixed(2) + " s");
                $("#TrainingEpoch").progressbar("value", data.current_epoch - 1);
                $("#TrainingEpochCount").html(
                    data.current_epoch + " / " +
                    $("#TrainingEpoch").progressbar("option", "max") + " | " +
                    $("#TrainingEpoch").find( ".ui-progressbar-value" ).text()
                );
            }
        },
        error_func,
        () => {
            if (isErrorHappen) {
                alert_func("Fail Get Training Process", "red", 3000);
                $("#TrainingStatus").html("Training Fail");
                isErrorHappen = false;
            }
        }
    );
}

function TrainModel() {
    $("#TrainingStartTime").html(new Date().toLocaleString());
    TrainingBoardOpenClose(true);
    trainingProcessObject = setInterval(trainingProcess, 1000);
    trainingProcess();

    ajax_func(
        "/model/" + projectName + "/train",
        "POST",
        {},
        (data) => {
            console.log(data);
            alert_func("Success Training Model", "#0dff00", 3000);
            $("#TrainingStatus").html("Finish Training");
            let progressBarMax = $("#TrainingEpoch").progressbar("option", "max")
            $("#TrainingEpoch").progressbar("value", progressBarMax);
            $("#TrainingEpochCount").html(
                progressBarMax + " / " + progressBarMax + " | " + "100.00 %"
            );
            clearInterval(trainingProcessObject);
            evalutionProcess();
        },
        (xhr, textStatus, errorThrown) => {
            if (xhr.responseText == "Training data not exist!") {
                alert_func(xhr.responseText, "yellow", 3000);
            } else if (xhr.responseText == "Test data not exist!") {
                alert_func(xhr.responseText, "yellow", 3000);
            } else {
                alert_func(xhr.responseText, "red", 3000);
                $("#train_model p").html("Build Model");
            }
            $("#TrainingStatus").html("Training Fail" + xhr.responseText);
            clearInterval(trainingProcessObject);
        },
        () => {}
    );
}

function evalutionProcess() {
    let isEvalutionSuccess = false;
    ajax_func(
        "/model/" + projectName + "/evaluate",
        "POST",
        {},
        successSendFile,
        error_func,
        () => {
            if (isErrorHappen) {
                alert_func("Fail To Evalution", "red", 3000);
                isErrorHappen = false;
            } else {
                console.log("Success Evalution");
                alert_func("Success Evalution", "Green", 3000);
                isEvalutionSuccess = true;
            }
        }
    );
}

$("#ModelSetting").click(() => {
    $("#TrainingSetting, #TrainingBoardBack").fadeIn();
    $("#TrainingSetting").css("display", "flex");
});

$("#train_model").click(() => {
    if ($("#train_model p").html() == "Train Model") {
        TrainModel();
    } else {
        $("#TrainingSetting, #TrainingBoardBack").fadeIn();
        $("#TrainingSetting").css("display", "flex");
    }
});

$("#TrainingSettingBtn").on("click", () => {
    if ($("#TrainingSetting input").val() == "") {
        alert_func("Input not allow empty value", "yellow", 3000);
        return;
    }

    let batch_size = parseInt($("#SettingBatchSize").val());
    let epochs = parseInt($("#SettingEpoch").val());
    let loss = $("#SettingLoss").val();
    let optimizer = $("#SettingOptimizer").val();
    let validation_split = parseFloat($("#SettingValidationSplit").val());

    $("#TrainingModelDetail").children("optgroup").each((key, value)=>{
        let frontText = ""
        if (key == 0) frontText = `BatchSize: ${batch_size}`;
        if (key == 1) frontText = `Epoch: ${epochs}`;
        if (key == 2) frontText = `Loss: ${loss}`;
        if (key == 3) frontText = `Optimizer: ${optimizer}`;
        if (key == 4) frontText = `Validation Split: ${validation_split}`;
        $(value).attr("label", frontText)
    })
    
    $("#TrainingEpoch").progressbar("option", "max", parseInt($("#SettingEpoch").val()));
    $("#TrainingEpoch").progressbar("value", false);
    $("#TrainingEpochCount").html(
        0 + " / " + 
        $("#TrainingEpoch").progressbar("option", "max") + " | " +
        $("#TrainingEpoch").find( ".ui-progressbar-value" ).text()
    );
    $("#TrainingStatus").html("Initialization");
    Create_Model_File();
});

function exportModel() {
    // ajax_func(
    //     "/model/" + projectName + "/exportModel",
    //     "POST",
    //     {},
    //     (data, textStatus) => {
    //         const content = Buffer.from(data, "hex");
    //         let file = new Blob([content], {type: "application/zip"});
    //         let a = document.createElement("a");
    //         a.href = URL.createObjectURL(file);
    //         a.download = "model.zip";
    //         a.style.display = "none";
    //         document.body.appendChild(a);
    //         a.click();
    //     },
    //     (xhr, textStatus, errorThrown) => {
    //         alert_func(xhr.responseText, "red", 3000);
    //     },
    //     () => {}
    // )

    $.ajax({
        url: "/model/" + projectName + "/exportModel",
        type: 'POST',
        data: JSON.stringify({}),  
        contentType: 'application/json', 
        xhrFields:{
            responseType: 'blob'
        },
        success: function(data){
            let a = document.createElement("a");
            let url = window.URL || window.webkitURL;
            a.href = url.createObjectURL(data);
            a.download = 'model.zip';
            a.style.display = "none";
            document.body.appendChild(a);
            a.click();
            setTimeout(function(){  
                document.body.removeChild(a);
                url.revokeObjectURL(a.href);
            }, 1);
        },
        error:function(){}
    });
}

$("#TrainingExportBtn").on("click", () => {
    ajax_func(
        "/model/" + projectName + "/checkExportModelExist",
        "POST",
        {},
        (data) => {
            if (data == "Model has been exported.") {
                exportModel();
            } else if (data == "Model has not been exported.") {
                exportModel();
            } else {
                console.log(data);
            }
            
        },
        error_func,
        () => {
            if (isErrorHappen) {
                alert_func("Fail To Export Model", "red", 3000);
                isErrorHappen = false;
            }
        }
    );
});

$("#save_graphy").click(() => {
    let graphy_package = {
        graphy: graphyPackage(),
    };
    console.log(graphy_package);
    if (graphy_package.graphy.length) {
        ajax_func(
            "/model/" + projectName + "/saveGraphy",
            "POST",
            graphy_package,
            successSendFile,
            error_func,
            () => {
                if (isErrorHappen) {
                    alert_func("Fail To Save Graphy", "red", 3000);
                    isErrorHappen = false;
                } else {
                    console.log("Success Save Graphy");
                    alert_func("Success Save Graphy", "Green", 3000);
                    isGraphySave = true;
                }
            }
        );
    }
});

/* 

    Training Board Function

*/

$("#BackToIndex").on("click", BackToIndex); // On Training Board

let TrainingBoard_IsOpen = false;

function TrainingBoardOpenClose(openOrNot) {
    if (openOrNot) {
        if (TrainingBoard_IsOpen) return;
        $("#TrainingBoard, #TrainingBoardBack").fadeIn();
        $("#TrainingBoard, #TrainingBoardBack").css("display", "block");
        setTimeout(() => {
            TrainingBoard_IsOpen = true;
        }, 300);
    } else {
        TrainingBoard_IsOpen = false;
        $("#TrainingBoard, #TrainingBoardBack").fadeOut();
    }
}

$("#TrainingEpoch").progressbar({
    value: false,
    change: () => {
        let target = $("#TrainingEpoch");
        target.find( ".ui-progressbar-value" )
            .text(
                (
                    target.progressbar("value") * 100 /
                    target.progressbar("option", "max")
                ).toFixed(2) + "%"
            );
    },
    complete: () => {
        $("#TrainingEpoch").find( ".ui-progressbar-value" ).text("Prograss Done!");
    }
})

$("#AccChart").on("click", () => {
    $("#TrainingImage").fadeIn();
    $("#TrainingImage img").attr("src", `/model/${projectName}/getImage?name=acc&rand=${new Date().getTime()}`);
    $("#TrainingImage img").attr("title", "acc");
    $("#TrainingImage").css("display", "flex");
});

$("#LossChart").on("click", () => {
    $("#TrainingImage").fadeIn();
    $("#TrainingImage img").attr("src", `/model/${projectName}/getImage?name=loss&rand=${new Date().getTime()}`);
    $("#TrainingImage img").attr("title", "loss");
    $("#TrainingImage").css("display", "flex");
});

$("#MetricsChart").on("click", () => {
    $("#TrainingImage").fadeIn();
    $("#TrainingImage img").attr("src", `/model/${projectName}/getImage?name=metrics&rand=${new Date().getTime()}`);
    $("#TrainingImage img").attr("title", "loss");
    $("#TrainingImage").css("display", "flex");
});

$("#TrainingImage").on("click", () => {
    $("#TrainingImage").fadeOut();
});

$("#TrainingBoardBack").on("click", () => {
    TrainingBoardOpenClose(false);
    $("#TrainingSetting").fadeOut();
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

let initialProcess = false  // get graphy process
let initItemId = 0;
let initPointID = 0; // initPointID for droparea item
let selectItem = null; // select item for del
let dropItemPointDown = []; // record select item point
let connectingLine = []; // record two point vector
let isInputLayerPlace = false;
let isGraphySave = false;
let SettingOpen = null;

function dragReflesh(element) {
    if (connectingLine.length) {
        // if has line connected
        mySVG.redrawLines();
    }
    // check the element size and scale the parent size
    setDropAreaSize();

    // set scrollbar position
    let offset = $(element).offset();
    $(".modelshow").scrollTop(offset.top);
    $(".modelshow").scrollLeft(offset.left);
}

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
                // Cannot place more than two Input Layer
                alert_func("無法放置一個以上的 Input Layer", "red", 3000);
                return;
            }
            clone.html(`
                <div></div>
                ${clone.html()}
                <div id="p${initPointID}" class="dropItemPoint dropItemPointRight"></div>
                <div class="dropItemMenu">
                    <div>Setting</div>
                    <div class="dropItemMenuLine">
                        <div>Width：</div>
                        <input type="Number" name="Width" value="32" />
                    </div>
                    <div class="dropItemMenuLine">
                        <div>Height：</div>
                        <input type="Number" name="Height" value="32" />
                    </div>
                </div>
            `);
            initPointID += 1;
            isInputLayerPlace = true;
        } else {
            clone.html(`
                <div id="p${initPointID}" class="dropItemPoint dropItemPointLeft"></div>
                ${clone.html()}
                <div id="p${
                    initPointID + 1
                }" class="dropItemPoint dropItemPointRight"></div>
                <div class="dropItemMenu">
                    <div>Setting</div>
                    ${layerParameter(clone.html())}
                </div>
            `);
            initPointID += 2;
        }

        // reset position
        let offset = $(this).offset();
        clone.css("top", `calc(${clone.css("top")} - ${offset.top}px)`);
        clone.css("left", `calc(${clone.css("left")} - ${offset.left}px)`);

        // right click menu
        clone.on("contextmenu", (event) => {
            event.preventDefault();
            closeDropMenu();
            $(clone).children(".dropItemMenu").css("display", "flex");
            SettingOpen = $(clone).children(".dropItemMenu");
            $(clone).css("z-index", 20);
            $(clone).css("opacity", 1);
        });

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
                    connectTwoLine(dropItemPointDown[0], dropItemPointDown[1]);
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

                // check if click dropItem
                if (
                    !(
                        $(event.target).parent().hasClass("dropItemMenu") ||
                        $(event.target).parent().hasClass("dropItemMenuLine") ||
                        $(event.target).hasClass("dropItemMenu")
                    )
                ) {
                    // set selectItem to target & set target border
                    selectItem = event.target;
                    $(selectItem).css("border", "1px dashed white");
                }
            }
        });

        // drag event for drop element
        clone.draggable({
            drag: function () {
                dragReflesh(this);
                isGraphySave = false;
            },
            stop: function (event, ui) {
                if (ui.position.top < 0) {
                    $(this).css('top', 0 + 'px');
                }
                if (ui.position.left < 0) {
                    $(this).css('left', 0 + 'px');
                }
                dragReflesh(this);
            },
            cancel: "div .dropItemPoint, input, select",
            scroll: true,
            cursor: "move",
            snap: true,
        });

        // add drop element to droparea
        $(this).append(clone);
        setInputChangeEvent();
        isGraphySave = false;
        who_are_dragging = "";
    },
});

function twoPointCheck(p1, p2) {
    let c1 = getConnectElementIndex(p1);
    let c2 = getConnectElementIndex(p2);

    // check if two-point is connected
    if (c1 != -1 && c1 == c2) {
        // Line is connected.
        alert_func("線已經連接", "yellow", 3000);
        $(p1).css("background-color", "unset");
        dropItemPointDown = [];
        return false;
    }

    // check if two-point parent is same
    if ($(p1).parent().attr("id") == $(p2).parent().attr("id")) {
        // Same layer cannot connect together.
        alert_func("相同 Layer 無法連在一起", "yellow", 3000);
        $(p1).css("background-color", "unset");
        dropItemPointDown = [];
        return false;
    }

    // check if one point connected
    if (c1 != -1) {
        deleteOneLine(p1);
    }
    if (c2 != -1) {
        deleteOneLine(p2);
    }
    return true;
}

function connectTwoLine(p1, p2) {
    if (!twoPointCheck(p1, p2)) {
        return;
    }
    // draw
    drawOneLine(p1, p2, "#ff8d8d");
    // append vector
    connectingLine.push([p1, p2]);
    // clear value
    $(p1).css("background-color", "unset");
    $(p2).css("background-color", "unset");
    dropItemPointDown = [];
    isGraphySave = false;
}

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

function closeDropMenu() {
    $(".dropItemMenu").css("display", "none");
    if (SettingOpen != null) {
        $(SettingOpen).parent().css("z-index", 10);
        $(SettingOpen).parent().css("opacity", 0.7);
        SettingOpen = null;
    }
}

function setInputChangeEvent() {
    $("input:not(#CBFile)").change(() => {
        isGraphySave = false;
    })
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

function deleteOneLine(pointId) {
    let index = getConnectElementIndex(pointId);
    if (index != -1) {
        // trigger canvas deleteLine
        mySVG.deleteLine({
            left_node: "#" + $(connectingLine[index][0]).attr("id"),
            right_node: "#" + $(connectingLine[index][1]).attr("id"),
        });

        // delete element from List
        connectingLine.splice(index, 1);

        // redraw canvas
        mySVG.redrawLines();
        return true;
    }
    return false;
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
    return $(vector[0]).attr("id") == $(point).attr("id")
        ? vector[1]
        : vector[0];
}

function getLayerMenu(Layer) {
    let tempDict = { layer_type: Layer.attr("name") };
    Layer
        .children(".dropItemMenu")
        .children(".dropItemMenuLine")
        .each((key, value) => {
            let temp = $(value).children("input");
            if (temp.length) {
                // case for checkbox and normal input
                if (temp.attr("type") == "checkbox") {
                    tempDict[temp.attr("name")] = temp.is(":checked");
                } else if (temp.attr("type") == "number") {
                    tempDict[temp.attr("name")] = parseFloat(temp.val());
                } else {
                    tempDict[temp.attr("name")] = temp.val();
                }
            } else {
                // case for select
                temp = $(value).children("select");
                tempDict[temp.attr("name")] = temp.val();
            }
        });
    return tempDict;
}

function putSetIntoMap(LayerMap, parent1, parent2, point1_id) {
    if (!LayerMap.has(parent1.attr("id"))) {
        LayerMap.set(parent1.attr("id"), {
            name: parent1.attr("id"),
            posX: parent1.position().left,
            posY: parent1.position().top,
            point_L_con: [],
            point_R_con: [],
            dictValue: getLayerMenu(parent1)
        });
    }
    if ($(point1_id).hasClass("dropItemPointLeft")) {
        LayerMap.get(parent1.attr("id")).point_L_con.push(parent2.attr("id"));
    } else {
        LayerMap.get(parent1.attr("id")).point_R_con.push(parent2.attr("id"));
    }
    return LayerMap;
}

/*

{
    posX: 0,
    posY: 0,
    point_L_con: [item_1],
    point_R_con: [item_2],
    dictValue: {
        layer_type: layerName,
        ...
    }
}

*/

function graphyPackage() {
    let LayerMap = new Map();
    // Find connected item
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

    // Find didn't connected item
    $(".dropItem").each((key, value) => {
        let element = $(value);
        if (!LayerMap.has(element.attr('id'))) {
            LayerMap.set(element.attr("id"), {
                posX: element.position().left,
                posY: element.position().top,
                point_L_con: [],
                point_R_con: [],
                dictValue: getLayerMenu(element)
            });
        }
    });

    // Map Convert to List
    let Result = [];
    for (const [, value] of LayerMap) {
        Result.push(value);
    }
    return Result;
}

function graphyUnpackage(package) {
    if (!Array.isArray(package)) {
        return False
    }
    let droparea = $('#droparea');
    let record_connect_line = [];

    // 1. Generate Item On Droparea
    package.forEach((element) => {
        // 1. Generate Item On Droparea
        let layer_type = element.dictValue.layer_type;
        let item = $(`<div class="${findLayerClassUseLayerName(layer_type)} dropItem">${layer_type}</div>`);
        // set item attr id, name
        item.attr("id", element.name);
        item.attr("name", layer_type);
        // set item position
        item.css("position", "absolute");
        item.css("left", element.posX);
        item.css("top", element.posY);
        // set max item id
        let elementId = parseInt(element.name.split('_')[1])
        if (initItemId < elementId) {
            initItemId = elementId + 1;
        }

        // set item html
        if (layer_type == "Input") {
            if (isInputLayerPlace) {
                // Cannot place more than two Input Layer
                alert_func("無法放置一個以上的 Input Layer", "red", 3000);
                return;
            }
            item.html(`
                <div></div>
                ${item.html()}
                <div id="p${initPointID}" class="dropItemPoint dropItemPointRight"></div>
                <div class="dropItemMenu">
                    <div>Setting</div>
                    <div class="dropItemMenuLine">
                        <div>Width：</div>
                        <input type="Number" name="Width" value="${element.dictValue.Width}" />
                    </div>
                    <div class="dropItemMenuLine">
                        <div>Height：</div>
                        <input type="Number" name="Height" value="${element.dictValue.Height}" />
                    </div>
                </div>
            `);
            initPointID += 1;
            isInputLayerPlace = true;
        } else {
            let jqObject = $(`<div>${layerParameter(item.html())}</div>`);
            Object.entries(element.dictValue).forEach(([key, val]) => {
                if (key == "layer_type") return;
                let findResult = jqObject.find(`input[name=${key}]`);
                if (findResult.length) {   // Input case
                    if (findResult.is("input[type='checkbox']")) {
                        findResult.prop('checked', val);
                    } else {
                        findResult.attr('value', val);
                    }
                } else {            // Select case
                    findResult = jqObject.find('select')
                    if (findResult.length) {
                        findResult.children(`[value='${val}']`).attr('selected', true);
                    }
                }
            });
            item.html(`
                <div id="p${initPointID}" class="dropItemPoint dropItemPointLeft"></div>
                ${item.html()}
                <div id="p${
                    initPointID + 1
                }" class="dropItemPoint dropItemPointRight"></div>
                <div class="dropItemMenu">
                    <div>Setting</div>
                    ${jqObject.html()}
                </div>
            `);
            initPointID += 2;
        }
        
        // right click menu
        item.on("contextmenu", (event) => {
            event.preventDefault();
            closeDropMenu();
            $(item).children(".dropItemMenu").css("display", "flex");
            SettingOpen = $(item).children(".dropItemMenu");
            $(item).css("z-index", 20);
            $(item).css("opacity", 1);
        });

        // click event for drop element
        item.click((event) => {
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
                    connectTwoLine(dropItemPointDown[0], dropItemPointDown[1]);
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

                // check if click dropItem
                if (
                    !(
                        $(event.target).parent().hasClass("dropItemMenu") ||
                        $(event.target).parent().hasClass("dropItemMenuLine") ||
                        $(event.target).hasClass("dropItemMenu")
                    )
                ) {
                    // set selectItem to target & set target border
                    selectItem = event.target;
                    $(selectItem).css("border", "1px dashed white");
                }
            }
        });

        // drag event for drop element
        item.draggable({
            drag: function () {
                dragReflesh(this);
                isGraphySave = false;
            },
            stop: function (event, ui) {
                if (ui.position.top < 0) {
                    $(this).css('top', 0 + 'px');
                }
                if (ui.position.left < 0) {
                    $(this).css('left', 0 + 'px');
                }
                dragReflesh(this);
            },
            cancel: "div .dropItemPoint, input, select",
            scroll: true,
            cursor: "move",
            snap: true,
        });

        // add drop element to droparea
        droparea.append(item);
        setInputChangeEvent();

        // record connect
        record_connect_line.push({
            left_item: element.point_L_con,
            right_item: element.point_R_con,
            this_item: element.name
        })
    });

    // 2. Connect Line
    record_connect_line.forEach((val) => {
        let item = $('#' + val.this_item)
        if (val.left_item.length) {
            let point_L = item.find(".dropItemPointLeft");
            val.left_item.forEach((each_item) => {
                let left_item = droparea.find('#' + each_item);
                connectTwoLine(point_L, left_item.find(".dropItemPointRight"));
            })
        }
        if (val.right_item.length) {
            let point_R = item.find(".dropItemPointRight");
            val.right_item.forEach((each_item) => {
                let right_item = droparea.find('#' + each_item);
                connectTwoLine(right_item.find(".dropItemPointLeft"), point_R);
            })
        }
    })

    return true;
}

function findLayerClassUseLayerName(layerName) {
    if (layerName == "Input") return "input_layer";
    if (layerName == "Conv2D") return "conv_layer";
    if (layerName == "Activation") return "activation_layer";
    if (layerName == "MaxPooling" || layerName == "AveragePooling") return "pooling_layer";
    if (layerName == "Flatten") return "reshaping_layer";
    if (layerName == "Dropout") return "regularization_layer";
    if (layerName == "Dense") return "core_layer";
    return "";
}

function getGraphy() {
    ajax_func(
        "/model/" + projectName + "/loadGraphy",
        "POST",
        "",
        (data) => {
            console.log(data);
            if (graphyUnpackage(data.graphy)) {
                console.log('Loading Success!');
                isGraphySave = true;
            } else {
                console.log('Loading Failure!');
            }
        },
        error_func,
        () => {
            if (isErrorHappen) {
                alert_func("Fail To Load Graphy", "red", 3000);
                isErrorHappen = false;
            }
        }
    );
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

function ModelPackage() {
    let point = $(".input_layer").children(".dropItemPointRight");
    let output_point = $(".core_layer").children(".dropItemPointLeft");
    let index = getConnectElementIndex(point);
    let input_parameter = $(".input_layer")
        .children(".dropItemMenu")
        .find("input");
    let layerList = [
        {
            layer_type: "Input",
            width: parseInt(input_parameter.eq(0).val()),
            height: parseInt(input_parameter.eq(1).val()),
        },
    ];

    if (index == -1) {
        alert_func("Input 需要連通", "red", 3000);
        return [];
    }

    // traverse the entire path
    while (index != -1) {
        // get another point and push layer name to layerList
        let ano_point = getAnotherPoint(connectingLine[index], point);
        let parent = $(ano_point).parent();
        layerList.push(getLayerMenu(parent));

        // set item left point or right point
        if ($(ano_point).hasClass("dropItemPointLeft")) {
            point = parent.children(".dropItemPointRight");
        } else {
            point = parent.children(".dropItemPointLeft");
        }

        index = getConnectElementIndex(point);
    }
    return layerList;
}

// key del method
function del_func() {
    if (selectItem != null) {
        connectingLine.forEach((value, index) => {
            if (
                $(value[0]).attr("id") == $(selectItem).find(".dropItemPointLeft").attr("id") ||
                $(value[1]).attr("id") == $(selectItem).find(".dropItemPointRight").attr("id")
            ) {
                connectingLine.splice(index, 1);
            }
        });
        $(selectItem).remove();
        isGraphySave = false;

        if ($(selectItem).html().includes("Input")) {
            isInputLayerPlace = false;
        }
        setDropAreaSize();
        // redraw canvas
        if (connectingLine.length) {
            // if has line connected
            mySVG.redrawLines();
        }
        selectItem = null;
    }

    if (dropItemPointDown.length > 0) {
        // Check is element connected
        if (deleteOneLine(dropItemPointDown[0])) {
            // If it connected, clear dropItemPointDown list
            dropItemPointDown[0].css("background-color", "unset");
            dropItemPointDown = [];
            isGraphySave = false;
        }
    }
}

/*

    Document ready

*/

$(document).ready(function() {
    getGraphy();
    setTimeout(() => { 
        initialProcess = true;
        setDropAreaSize();
    }, 1000);
});

/*

    Close event

*/

window.addEventListener('beforeunload', (event) => {
    if (!isGraphySave) {
        event.preventDefault();
        event.returnValue = "";
    }
});

/*

    Alert Dialog

*/

function alert_func(msg, color, closeTime) {
    if (!initialProcess) {
        console.log(msg);
        return;
    }
    $("#AlertDialog").css("background-color", color);
    $("#AlertDialog").html(msg);
    $("#AlertDialog").toggle("blind");
    $("#AlertDialog").effect("bounce");
    setTimeout(() => {
        $("#AlertDialog").toggle("blind");
    }, closeTime);
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
    if ($("canvas")) {
        $("canvas").attr("width", $(".modelshow").width())
        $("canvas").attr("height", $(".modelshow").height())
        if (connectingLine.length) {
            // if has line connected
            mySVG.redrawLines();
        }
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

    if (SettingOpen != null) {
        if (!$(event.target).closest(SettingOpen).length) {
            closeDropMenu();
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
    let target = "#CenterBoard, #ChooseTrain, #ChooseTest";
    if (!$(event.target).closest(target).length) {
        $("#CenterBoard").css("display", "none");
        OpenCloseCenterBoard(false, "");
    }
});

function layerParameter(layerName) {
    let parameter = layerDict[layerName];
    let tempHtml = "";
    if (Array.isArray(parameter)) {
        parameter.forEach((val) => {
            if (val.type == "select") {
                option_html = "";
                val.initVal.forEach((element) => {
                    option_html += `<option value="${element}">${element}</option>`;
                });
                tempHtml += `
                <div class="dropItemMenuLine">
                    <div>${val.name}：</div>
                    <select name="${val.name}">${option_html}</select>
                </div>`;
            } else {
                tempHtml += `
                <div class="dropItemMenuLine">
                    <div>${val.name}：</div>
                    <input 
                        type="${val.type}" 
                        name="${val.name}" 
                        value="${val.initVal}" 
                        ${"min" in val ? "min=" + val.min : ""}
                        ${"max" in val ? "max=" + val.max : ""}
                        ${"step" in val ? "step=" + val.step : ""}
                    />
                </div>`;
            }
        });
        return tempHtml;
    } else {
        console.log(layerName + "Not a List");
        return "";
    }
}
