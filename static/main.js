$(function () {
    // test to ensure jQuery is working
    console.log("whee!")

    // // disable refresh button
    // $("#refresh-btn").prop("disabled", true)

    $("#course_link").hide();
    $("#branch_link").hide();
    $("#semester_link").hide();
    $("#college_link").show();
    
    $("#course_link2").hide();
    $("#branch_link2").hide();
    $("#semester_link2").hide();
    $("#college_link2").show();

    $("#show_table").hide();


    $("#college").change(function () {
        $("#course_link").show();
        $("#branch_link").hide();
        $("#semester_link").hide();
        $("#college_link").hide();

        $("#course_link2").show();
        $("#branch_link2").hide();
        $("#semester_link2").hide();
        $("#college_link2").hide();

        // grab value
        var college_id = $("#college").val();

        // send value via GET to course/<college_id>

        var get_request = $.ajax({
            type: 'GET',
            url: '/course/' + college_id + '/',
        });

        // handle response
        get_request.done(function (data) {

            // data
            console.log(data)

            // add values to list 
            var option_list = [["", "", "Choose..."]].concat(data);
            $("#course").empty();
            for (var i = 0; i < option_list.length; i++) {
                $("#course").append(
                    $("<option></option>").attr("value", option_list[i][0]).text(option_list[i][2]));
            }
            // show model list
            $("#course_link").attr("href", "/select/course/" + college_id);
            $("#course").show();
        });
    });

    $("#course").change(function () {

        $("#course_link").hide();
        $("#branch_link").show();
        $("#semester_link").hide();
        $("#college_link").hide();

        $("#course_link2").hide();
        $("#branch_link2").show();
        $("#semester_link2").hide();
        $("#college_link2").hide();


        // grab value
        var course_id = $("#course").val();

        // send value via GET to branch/<course_id>

        var get_request = $.ajax({
            type: 'GET',
            url: '/branch/' + course_id + '/',
        });

        // handle response
        get_request.done(function (data) {

            // data
            console.log(data)

            // add values to list 
            var option_list = [["", "", "Choose..."]].concat(data);
            $("#branch").empty();
            for (var i = 0; i < option_list.length; i++) {
                $("#branch").append(
                    $("<option></option>").attr("value", option_list[i][0]).text(option_list[i][2]));
            }
            // show model list
            $("#branch_link").attr("href", "/select/branch/" + course_id);
            $("#branch").show();
        });
    });

    $("#branch").change(function () {

        $("#course_link").hide();
        $("#branch_link").hide();
        $("#semester_link").show();
        $("#college_link").hide();

        $("#course_link2").hide();
        $("#branch_link2").hide();
        $("#semester_link2").show();
        $("#college_link2").hide();

        // grab value
        var branch_id = $("#branch").val();

        // send value via GET to semester/<branch_id>

        var get_request = $.ajax({
            type: 'GET',
            url: '/semester/' + branch_id + '/',
        });

        // handle response
        get_request.done(function (data) {

            // data
            console.log(data)

            // add values to list 
            var option_list = [["", "", "Choose..."]].concat(data);
            $("#semester").empty();
            for (var i = 0; i < option_list.length; i++) {
                $("#semester").append(
                    $("<option></option>").attr("value", option_list[i][0]).text(option_list[i][2]));
            }
            // show model list
            $("#semester_link").attr("href", "/select/semester/" + branch_id);
            $("#semester").show();
        });
    });
    
    $("#semester").change(function () {

        $("#course_link").hide();
        $("#branch_link").hide();
        $("#semester_link").hide();
        $("#college_link").hide();

        $("#course_link2").hide();
        $("#branch_link2").hide();
        $("#semester_link2").hide();
        $("#college_link2").hide();

        $("#show_table").show();


        // grab value
        var semester_id = $("#semester").val();
              
        //send value via GET to semester/<branch_id>

        

        // // handle response
        // get_request.done(function (data) {

        //     // data
        //     console.log(data)

        //     // add values to list 
        //     var option_list = [["", "", "Choose..."]].concat(data);
        //     $("#semester").empty();
        //     for (var i = 0; i < option_list.length; i++) {
        //         $("#semester").append(
        //             $("<option></option>").attr("value", option_list[i][0]).text(option_list[i][2]));
        //     }
        //     // show model list
        //     $("#semester_link").attr("href", "/select/semester/" + branch_id);
        //     $("#semester").show();
        // });
    });
    // $("#show_table").click(function(){
    //     var get_request = $.ajax({
    //         type: 'POST',
    //         url: '/timetable/' + 1 + '/',
    //     });
        
    // });

});