var spotButton = $("#spotButton");
var infoButton = $("#infoButton");


spotButton.click(function() {
    console.log(spotButton.text());
    $.ajax({
        url: "/spotify",
        type: "post",
        success: function(response) {
            console.log(response);
        }
    });
});


infoButton.click(function () {
    console.log(infoButton.text());
    $.ajax({
        url: "/pi_info",
        type: "post",
        success: function (response) {
            console.log(response);
        }
    });
});
