$(document).ready(function () {
  var latex, latex_start, comparison_result, final_result, strokes, strokes2, strokes3
  $(function () {
    function transform(strokes) {
      for (var i = 0; i < strokes.length; ++i)
        for (var j = 0, stroke = strokes[i]; j < stroke.length; ++j)
          strokes[i][j] = [strokes[i][j][0], strokes[i][j][1]];
      return strokes;
    };

    function urlParam(name) {
      var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(top.window.location.href);
      return (results !== null) ? results[1] : undefined;
    };

    // Canvas 1

    var $canvas = $('#drawing-canvas').sketchable({
      graphics: {
        strokeStyle:  "black",
        firstPointSize: 1,
        lineWidth: 1
      }
    });

    function clearStrokes() {
      $canvas.sketchable('clear');
      $('.result').empty();
    };

    function submitStrokes() {
      var strokes = $canvas.sketchable('strokes');
      // Submit strokes in the required format.
      var strokes2 = transform(strokes);
      var strokes3 = strokesToScg(strokes2);
      $.ajax({
        type: "POST",
        url: '/new_task',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        async: false,
        //json object to sent to the authentication url
        data: JSON.stringify(strokes3),
        beforeSend: function (xhr) {
          console.log("Wait...")
        },
        finish: function (data) {
          console.log("Finish! LaTeX: " + data);
        },

        success: function (data) {
          console.log("Sucess! LaTeX: " + data);
          console.log(typeof data)
          latex_start = data.replace(/ /g, '');
        }
      })
    };

    //Canvas 2

    var $canvas2 = $('#canvas-active').sketchable({
      graphics: {
        strokeStyle: "blue",
        firstPointSize: 1,
        lineWidth: 1
      }
    });


    function clearStrokes2() {
      $canvas2.sketchable('clear');
      $('.result').empty();
    };


    function submitStrokes2() {
      strokes = $canvas2.sketchable('strokes');
      // Submit strokes in the required format.
      strokes2 = transform(strokes);
      strokes3 = strokesToScg(strokes2);
      $.ajax({
        type: "POST",
        url: '/comparison',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        async: false,
        //json object to sent to the authentication url
        data: JSON.stringify(strokes3),
        beforeSend: function (xhr) {
          console.log("Wait...")
        },
        finish: function (data) {
          console.log("Finish! LaTeX: " + data);
        },

        success: function (data) {
          var received_data = JSON.parse(JSON.stringify(data));
          console.log("Sucess! LaTeX: " + received_data);
          console.log(typeof received_data)
          latex = received_data["eq_middle"].replace(/ /g, '');
          comparison_result = received_data["comparison_result"];
        }
      })
    };

    function replace_canvas() {
      $('#canvas-active').removeAttr('id');
      $('#send_equation2').removeAttr('id');
      $('#clear2').removeAttr('id');

      $("#main .row .col-8")
        .append('<div class="app draw"><div class="btn-group-vertical controls" role="group" aria-label="Basic example"><button id="send_equation2" class="test-button btn btn-warning btn-block">NEXT</button></div><canvas id="canvas-active" class="drawing-canvas-extend" width=600 height=100></canvas><div class="btn-group-vertical controls" role="group" aria-label="Basic example"><button id="clear2" class="clear-button btn btn-warning" >CLEAR</button></div></div>');

      $canvas2 = $('#canvas-active').sketchable({
        graphics: {
          strokeStyle: "blue",
          firstPointSize: 1,
          lineWidth: 1
        }
      });

      function clearStrokes2() {
        $canvas2.sketchable('clear');
      };

      $('#send_equation2').on("click", function () {
        submitStrokes2();
        $('#eq-extend').append('<div style="height: 100px;" class="d-flex justify-content-center align-items-center"><img src="http://latex.codecogs.com/svg.latex?' + latex + '" border="0" min-height="30px"/></div>');
        if(comparison_result == true) {
          $('#eq-extend div:last-child').css("background-color","rgba(0, 128, 0, 0.5)");
        } else {
          $('#eq-extend div:last-child').css("background-color","rgba(255, 0, 0, 0.5)");
        }
        $('#clear2').hide();
        $('#send_equation2').hide();
        $('#canvas-active').css("background-color","transparent");
        $('#canvas-active').css("z-index","-999");
        replace_canvas();
      });

      $('#clear2').on("click", function (e) {
        e.preventDefault();
        clearStrokes2();
      });



    }

    //Canvas 3

    var $canvas3 = $('#drawing-canvas3').sketchable({
      graphics: {
        strokeStyle: "black",
        firstPointSize: 1,
        lineWidth: 1
      }
    });


    function clearStrokes3() {
      $canvas3.sketchable('clear');
      $('.result').empty();
    };


    function submitStrokes3() {
      var strokes = $canvas3.sketchable('strokes');
      // Submit strokes in the required format.
      var strokes2 = transform(strokes);
      var strokes3 = strokesToScg(strokes2);
      $.ajax({
        type: "POST",
        url: '/result',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        async: false,
        //json object to sent to the authentication url
        data: JSON.stringify(strokes3),
        success: function (data) {
          var received_data = JSON.parse(JSON.stringify(data));
          console.log("Sucess! LaTeX: " + received_data);
          console.log(typeof received_data)
          latex = received_data["eq_end"].replace(/ /g, '');
          final_result = received_data["comparison_result"];
          if (final_result == true) {
            final_result = "You solved the task. Congrats!"
          }

        }
      })
    };


      //Canvas 4

      var $canvas4 = $('#drawing-canvas4').sketchable({
        graphics: {
          strokeStyle: "black",
          firstPointSize: 1,
          lineWidth: 1
        }
      });

    function strokesToScg(strokes) {
      var scg = 'SCG_INK\n' + strokes.length + '\n'
      strokes.forEach(function (stroke) {
        scg += stroke.length + '\n'
        stroke.forEach(function (p) {
          scg += p[0] + ' ' + p[1] + '\n'
        })
      })

      return scg
    }


    $('#send_equation').on("click", function () {
      submitStrokes();
      latex_start = latex_start.replace(/\\\\/g, "\\");
      $('#eq-start').append('<img src="http://latex.codecogs.com/svg.latex?' + latex_start + '" border="0" height="20px"/>')
      $('#clear1').hide();
      $('#send_equation').hide();
      $('#main').show();
      $('#result-eq').show();
      $('#drawing-canvas').css("background-color","transparent");
      $('#drawing-canvas').css("z-index","-999");
      $('#i1').hide();
      $('#i2').show();
      $('#i3').show();
      $('#i0').hide();
      $('#i4').show();
      $('#i5').show();
    });

    $('#send_equation2').on("click", function () {
      submitStrokes2();
      latex = latex.replace(/\\\\/g, "\\");
      $('#eq-extend').append('<div style="height: 100px;" class="d-flex justify-content-center align-items-center"><img src="http://latex.codecogs.com/svg.latex?' + latex + '" border="0" height="20px"/></div>');
      if(comparison_result == true) {
        $('#eq-extend div:last-child').css("background-color","rgba(0, 128, 0, 0.5)");
      } else {
        $('#eq-extend div:last-child').css("background-color","rgba(255, 0, 0, 0.5)");
      }
      $('#clear2').hide();
      $('#send_equation2').hide();
      $('#canvas-active').css("background-color","transparent");
      $('#canvas-active').css("z-index","-999");
      replace_canvas();
    });

    $('#send_equation3').on("click", function () {
      submitStrokes3();
      latex = latex.replace(/\\\\/g, "\\");
      // $('input[name="eq_final_1"]').val(latex);
      $('#eq-end').append('<img src="http://latex.codecogs.com/svg.latex?' + latex + '" border="0"/><p class="ml-4">' + final_result + '</p>')
    });

    $('#send_equation4').on("click", function jj() {
      submitStrokes3();
      latex = latex.replace(/\\\\/g, "\\");
      $('input[name="eq_final_2"]').val(latex);
    });

    $('#clear').on("click", function (e) {
      e.preventDefault();
      clearStrokes();
    });

    $('#clear2').on("click", function (e) {
      e.preventDefault();
      clearStrokes2();
    });

    $('#clear3').on("click", function (e) {
      e.preventDefault();
      clearStrokes3();
    });

    $('a#send').on("click", function (e) {
      e.preventDefault();
      submitStrokes();
    });

    $('a#undo').on("click", function (e) {
      e.preventDefault();
      $canvas.sketchable('undo');
    });

    $('a#redo').on("click", function (e) {
      e.preventDefault();
      $canvas.sketchable('redo');
    });

    if (urlParam("train")) {
      // Shortcut to clear canvas + submit strokes.
      $(document).on("keydown", function (e) {
        //if (e.ctrlKey && e.which == 65) { // This can be exhausting.
        if (e.which == 45 || e.which == 96) { // Better be pressing a single key, e.g. INS.
          e.preventDefault();
          submitStrokes();
          clearStrokes();
        }
      });
    }

  
  
    $('#main').hide();
  $('#result-eq').hide();
});
});