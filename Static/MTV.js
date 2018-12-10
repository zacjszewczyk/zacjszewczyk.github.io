// Variables
// - dimensions: Dimensions of the #box element, used to position elements relative to it.
// - MAGIC: Used to convert from feet to pixels. Multiply ft * MAGIC.
var dimensions;
const MAGIC = 31.5;

// Functions

// Method: adjustSize()
// Purpose: Adjust the box and window size. Call functions to adjust the rest of 
// the rig, as necessary.
// Parameters: none
function adjustSize() {
    // Get the value of the box length input field
    var field = document.getElementById("box_length_field").value;

    // If the box is between 12 and 14 feet long, inclusive:
    if (field >= 12 && field <= 14) {
        // This means we don't need the angled portion on the back, so hide it
        $("#container").hide();
        // Adjust the box size
        $("#box").show().width(field*MAGIC);
        // Adjust the window size, smaller for shorter rigs
        $("#aft_window").width(field*8);
    }
    // If the box is over 14 feet long:
    else if (field > 14) {
        // If the M1078 chassis is selected, set the box length to 14 feet and leave
        // the remainder for the angled portion on the back.
        if ($("#M1078").css("display") == "block") {
            $("#box").show().width(14*MAGIC);
        }
        // Otherwise, the M1083 box is selected:
        else {
            // If the M1083 chassis is selected, and the box length is (14,16], set 
            // the box length to the length specified. Hide the container.
            if (field <= 16) {
                $("#box").show().width(field*MAGIC);
                $("#container").hide();
            }
            // If the M1083 chassis is selected, and the box length is >16 feet,
            // set the box length to 16 feet and leave the remainder for the angled
            // portion on the back.
            else {                        
                $("#box").show().width(16*MAGIC);
            }
        }
        // Adjust the window size, larger for longer rigs
        $("#aft_window").width(field*12);
    }
    // Adjust the angled portion size, as necessary
    angledSize();
    // Adjust the topper size, as necessary
    adjustTopper();
    // Update the cookie
    updateCookie();
}
// Method: angledSize()
// Purpose: Adjust the rear cutoff size.
// Parameters: none
function angledSize() {
    // Depending on the chassis, we will either ignore the first 14 or 16 feet of
    // the box. The remaining distance will be made up with this angled portion.
    var offset = getChassis();

    // Get the value in the box length input field
    var field = document.getElementById("box_length_field").value;

    // Create a struct to store the box's dimensions
    dimensions = {width : parseInt($("#box").css("width")), height : parseInt($("#box").css("height")) };
    
    // Show the container
    $("#container").show();
    // Set the container dimensions
    // (field-offset)             = Length, in feet, of the angled portion.
    // (field-offset)*MAGIC       = Length, in pixels, of the angled portion
    // 0.839*(field-offset)*MAGIC = y-dimension of the angled portion, to be
    //                              subtracted from the box height. 0.839 is
    //                              slope of a 40 degree line.
    $("#container").css("height", 229-(0.839*(field-offset)*MAGIC));
    $("#container").css("width", (field-offset)*MAGIC);
    // Position the angled portion at the right edge of the box
    $("#container").css("left", dimensions.width);
    
    // Use border-width CSS attributes to create a line at a 40 degree angle
    // at the rear of the rig, to preserve approach/departure angles.
    $("#angled").css("border-width", (0.839*(field-offset)*MAGIC).toString()+"px "+((field-offset)*MAGIC).toString()+"px 0 0");
    // Position the angled portion at the bottom of the box
    $("#angled").css("top", dimensions.height-(0.839*(field-offset)*MAGIC));
}
// Method: getChassis()
// Purpose: Return 14 if the M1078 chassis is selected, and 16 if the M1083.
// Parameters: none
function getChassis() {
    if ($(".chassis")[0].checked == true) {
        return 14;
    } else {
        return 16;
    }
}
// Method: adjustTopper()
// Purpose: Adjust the topper size, based on the box size and position.
// Parameters: none
function adjustTopper() {
    // Size the topper to the box's width, minus a 250px offset, plus the width of
    // the angled portion on the rear of the rig.
    $("#topper").css("width", parseFloat($("#box").css("width").replace("px", ""))-250+parseFloat($("#container").css("width").replace("px", "")));
}
// Method: flip()
// Purpose: Toggle CSS to mirror the rig image horizontally, and toggle display of the
// door as necessary.
// Parameters:
// - element: The element to be flipped. Enables polymorphism.
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
// Method: gray()
// Purpose: Add CSS to color a specified image gray.
// Parameters:
// - element: The element to be colored. Enables polymorphism.
function gray(element) {
    $(element).css("filter", "invert(5%) grayscale(100%) brightness(90%) contrast(1)");
    updateCookie();
}
// Method: clearColor()
// Purpose: Remove CSS to color a specified image gray.
// Parameters:
// - element: The element to be cleared. Enables polymorphism.
function clearColor(element) {
    $(element).css("filter", "");
    updateCookie();
}
// Method: windows()
// Purpose: Show and hide windows, based on which window checkboxes are checked.
// Parameters: none.
function windows() {
    $.each($(".window:checked"), function (key,value) {
        $("#"+$(value).val()).show();
    });
    $.each($(".window:not(:checked)"), function (key,value) {
        $("#"+$(value).val()).hide();
    });
    updateCookie();
}
// Method: updateCookie()
// Purpose: Create a cookie to preserve rig state across sessions.
// Parameters: none.
function updateCookie() {
    var view = $(".view:checked").val();
    var chassis = $(".chassis:checked").val();
    var box = $("#box_length_field").val();
    var topper = $("#raised_roof_checkbox").val();
    var door = $(".door:checked").val();
    var chassis_color = $(".chassis_color:checked").val();
    var box_color = $(".box_color:checked").val();
    var passthrough = $(".passthrough:checked").val();
    var fore_window = $("#fore_window_checkbox:checked").val();
    var aft_window = $("#aft_window_checkbox:checked").val();
    document.cookie = "rv=view="+view+",chassis="+chassis+",box="+box+",topper="+topper+",door="+door+",chassis_color="+chassis_color+",box_color="+box_color+",passthrough="+passthrough+",fore_window="+fore_window+",aft_window="+aft_window+";";
    // console.log(document.cookie);
}
// Method: readCookie()
// Purpose: Return the RV cookie.
// Parameters: none.
function readCookie() {
    return document.cookie.split(";")[0].replace("rv=", "").split(",");
}
// Method: parseCookie()
// Purpose: Read the cookie and build the rig based off of a saved state.
// Parameters: none.
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
    if (cookie[8].split("=")[1] == "fore_window") {
        $("#fore_window_checkbox").prop("checked", "checked");
        $("#fore_window").show();
    }
    if (cookie[9].split("=")[1] == "aft_window") {
        $("#aft_window_checkbox").prop("checked", "checked");
        $("#aft_window").show();
    }
}
// Method: changeChassis()
// Purpose: Change chassis, and update max length value for the box length field.
// Parameters: none.
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
    // Windows
    $(".window").click(function () {
        windows();
    });

    // Reset
    $("#reset").click(function() {
        document.cookie = "rv=";
        location.reload();
    });
});