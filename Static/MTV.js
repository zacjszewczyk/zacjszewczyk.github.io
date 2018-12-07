// Variables
var position;
var dimensions;

const MAGIC = 31.5;

// Functions
function adjustSize() {
    var field = document.getElementById("box_length_field");

    if (field.value >= 12 && field.value <= 14) {
        angledSize();
        $("#container").hide();
        $("#box").show().width(field.value*MAGIC);
        adjustTopper();
    }
    else if (field.value > 14) {
        if ($("#M1078").css("display") == "block") {
            $("#box").show().width(14*MAGIC);
            angledSize();
        }
        else {
            if (field.value <= 16) {
                $("#box").show().width(field.value*MAGIC);
                angledSize();
                $("#container").hide();
            }
            else {                        
                $("#box").show().width(16*MAGIC);
                angledSize();
            }
        }
    }
    adjustTopper();
    updateCookie();
}
function angledSize() {
    var offset = 0;
    offset = getChassis();

    var field = document.getElementById("box_length_field");

    dimensions = {width : parseInt($("#box").css("width")), height : parseInt($("#box").css("height")) };
            
    $("#container").show();
    $("#container").css("height", 229-(0.839*(field.value-offset)*MAGIC));
    $("#container").css("width", (field.value-offset)*MAGIC);
    $("#angled").css("top", dimensions.height-(0.839*(field.value-offset)*MAGIC));
    $("#container").css("left", dimensions.width);
    $("#angled").css("border-width", (0.839*(field.value-offset)*MAGIC).toString()+"px "+((field.value-offset)*MAGIC).toString()+"px 0 0");
}
function getChassis() {
    if ($(".chassis")[0].checked == true) {
        return 14;
    } else {
        return 16;
    }
}
function adjustTopper() {
    $("#topper").css("width", parseFloat($("#box").css("width").replace("px", ""))-250+parseFloat($("#container").css("width").replace("px", "")));
}
function flip(element) {
    if ($(element).css("transform") == "none") {
        $("#images").css("-moz-transform", "scaleX(-1)");
        $("#images").css("-o-transform", "scaleX(-1)");
        $("#images").css("-webkit-transform", "scaleX(-1)");
        $("#images").css("transform", "scaleX(-1)");
        if ($(".door:checked").val() == "right") {
            $("#door").show();
        }
        else {
            $("#door").hide();   
        }
    }
    else
    {
        $("#images").css("-moz-transform", "");
        $("#images").css("-o-transform", "");
        $("#images").css("-webkit-transform", "");
        $("#images").css("transform", "");
        if ($(".door:checked").val() == "left") {
            $("#door").show();
        }
        else {
            $("#door").hide();   
        }
    }
}
function gray(element) {
    $(element).css("filter", "invert(5%) grayscale(100%) brightness(90%) contrast(1)");
    updateCookie();
}
function clearColor(element) {
    $(element).css("filter", "");
    updateCookie();
}
function updateCookie() {
    var view = $(".view:checked").val();
    var chassis = $(".chassis:checked").val();
    var box = $("#box_length_field").val();
    var topper = $("#raised_roof_checkbox").val();
    var door = $(".door:checked").val();
    var chassis_color = $(".chassis_color:checked").val();
    var box_color = $(".box_color:checked").val();
    var passthrough = $(".passthrough:checked").val();
    document.cookie = "rv=view="+view+",chassis="+chassis+",box="+box+",topper="+topper+",door="+door+",chassis_color="+chassis_color+",box_color="+box_color+",passthrough="+passthrough+";";
    // console.log(document.cookie);
}
function readCookie() {
    return document.cookie.split(";")[0].replace("rv=", "").split(",");
}
function parseCookie() {
    var cookie = readCookie();
    // console.log(cookie);
    if (cookie.length == 1) { $("#topper").hide(); return 0; };
    if (cookie[0].split("=")[1] == "right_view") {
        flip($("#images"));
    }
    $("#"+cookie[0].split("=")[1]).prop("checked", "checked");
    //
    if (cookie[1].split("=")[1] == "16") {
        $(".chassis").prop("checked", "unchecked");
        $("#M1083_button").prop("checked", "checked");
        changeChassis();
    }
    //
    if (cookie[2].split("=")[1] != "14") {
        $("#box_length_field").attr("value", cookie[2].split("=")[1]);
        if (cookie[2].split("=")[1] == "16") { 
            $(".box_length_checkbox").prop("checked", false);
            $("#16ft_box_button").prop("checked", true);
        }
    }
    //
    if (cookie[3].split("=")[1] == "block") {
        $("#raised_roof_checkbox").prop("checked", true)
        $("#raised_roof_checkbox").attr("value", "block")
        $("#topper").show();
    }
    else {
        $("#topper").hide();
    }
    //
    if (cookie[4].split("=")[1] == "right") {
        $("#door_right").prop("checked", true);
    }
    if (cookie[4].split("=")[1] != cookie[0].split("=")[1].split("_")[0]) {
        $("#door").hide();
    }
    else {
        $("#door").show();
    }
    if (cookie[5].split("=")[1] == "gray") {
        $("#chassis_gray").prop("checked", true);
        gray($(".chassis_images"));
    }
    if (cookie[6].split("=")[1] == "gray") {
        $("#box_gray").prop("checked", true);
        gray($("#box"));
    }
    if (cookie[7].split("=")[1] == "true") {
        $("#passthrough").show();
        $("#passthrough_true").prop("checked", true);
    }
}
function changeChassis() {
    $(".chassis_images").hide();
    var id = $(".chassis:checked").attr("id").split("_")[0];
    $("#"+id).show();
    if (id == "M1078") {
        if (document.getElementById("box_length_field").value > 21) {
            document.getElementById("box_length_field").value = 21;
        }
        $("#box_length_field").attr("max", 21);
    }
    else {
        $("#box_length_field").attr("max", 22);
    }
    adjustSize();
}

// End functions
$( document ).ready(function() {
    $("main").show();
    parseCookie();
    adjustSize();
    // View selector
    $(".view").click(function() {
        $("#images").css("transition", "transform 2s");
        flip($("#images"));
        updateCookie();
    });

    // Chassis selector
    $(".chassis").click(function() {
        changeChassis();
    });

    // Passthrough
    $(".passthrough").click(function() {
        $("#passthrough").toggle();
        updateCookie();
    });

    // Box length checkboxes
    $(".box_length_checkbox").click(function() {
        document.getElementById("box_length_field").value = this.value;
        adjustSize()
        $(".box_length_checkbox").prop("checked", false);
        $(this).prop("checked", true);
    });

    // Box length field
    $("#box_length_field").on('input', function() {
        $(".box_length_checkbox").prop("checked", false);
        if ((getChassis() == 14 && this.value <= 21) || (getChassis() == 16 && this.value <= 23)) {
            adjustSize();
        }
    });

    // Raised roof checkbox
    $("#raised_roof_checkbox").click(function() {
        $("#topper").toggle();
        this.value = $("#topper").css("display");
        updateCookie();
    });

    // Door
    $(".door").click(function () {
        if ($(".view:checked").val().split("_")[0] != $(".door:checked").val()) {
            $("#door").hide();
        }
        else {
            $("#door").show();
        }
        updateCookie();
    });

    // Color
    $(".chassis_color").click(function () {
        if ($(this).val() == "gray") {
            gray($(".chassis_images"));
        } else
        {
            clearColor($(".chassis_images"));
        }
    });
    $(".box_color").click(function () {
        if ($(this).val() == "gray") {
            gray($("#box"));
        } else
        {
            clearColor($("#box"));
        }
    });

    // Reset
    $("#reset").click(function() {
        document.cookie = "rv=";
        location.reload();
    });
});