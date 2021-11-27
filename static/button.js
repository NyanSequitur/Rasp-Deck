var button = $("#led_button");
button.click(function() {
    console.log(button.text());
    if (button.text() === "Spotify") {
        $.ajax({
            url: "/spotify",
            type: "post",
            success: function(response) {
                console.log(response);
                button.text("Pi Info");
            }
        });
    } else {
        $.ajax({
            url: "/pi_info",
            type: "post",
            success: function() {
                button.text("Spotify");
            }
        })
    }
});
