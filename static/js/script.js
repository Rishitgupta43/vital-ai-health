$(document).ready(function () {

    // Extract username from URL
    let username = window.location.pathname.split("/").pop();


    function addMessage(text, type) {

        let msg = $("<div>").addClass("message " + type);

        // Convert line breaks to proper spacing
        let formattedText = text.replace(/\n/g, "<br>");

        msg.html(formattedText);

        $("#ChatArea").append(msg);

        $("#ChatArea").scrollTop($("#ChatArea")[0].scrollHeight);
    }


    $("#chatForm").submit(function (e) {

        e.preventDefault();

        let msg1 = $("#message1").val();
        let msg2 = $("#message2").val();
        let msg3 = $("#message3").val();

        let sleep_hours = $("#sleep_hours").val();
        let sleep_quality = $("#sleep_quality").val();
        let wake_refreshed = $("#wake_refreshed").val();

        let exercise_freq = $("#exercise_freq").val();
        let exercise_type = $("#exercise_type").val();

        let diet_type = $("#diet_type").val();
        let processed_food = $("#processed_food").val();

        let alcohol = $("#alcohol").val();
        let smoking = $("#smoking").val();
        let caffeine = $("#caffeine").val();

        if (!msg1) return;

        $("#ChatArea").addClass("active");

        addMessage("🧑 " + msg1, "user");


        // Loading message
        let loading = $("<div class='message ai'>Analyzing...</div>");
        $("#ChatArea").append(loading);


        $.post("/ask/" + username, {

            message1: msg1,
            message2: msg2,
            message3: msg3,

            sleep_hours: sleep_hours,
            sleep_quality: sleep_quality,
            wake_refreshed: wake_refreshed,

            exercise_freq: exercise_freq,
            exercise_type: exercise_type,

            diet_type: diet_type,
            processed_food: processed_food,

            alcohol: alcohol,
            smoking: smoking,
            caffeine: caffeine

        })
        .done(function (data) {

            loading.remove();

            addMessage("🤖 " + data, "ai");

        })
        .fail(function () {

            loading.remove();

            addMessage("⚠️ Server error. Try again.", "ai");
        });


        // Clear inputs
        $("#message1, #message2, #message3").val("");
    });


    // Clear chat with animation
    $("#clearChat").click(function () {

        $("#ChatArea").fadeOut(300, function () {

            $(this).html("").removeClass("active").fadeIn(300);

        });

    });

});