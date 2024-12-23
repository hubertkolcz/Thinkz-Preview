  
var latex;
$(function(){

    function transform(strokes) {
      for (var i = 0; i < strokes.length; ++i)
        for (var j = 0, stroke = strokes[i]; j < stroke.length; ++j)
            strokes[i][j] = [ strokes[i][j][0], strokes[i][j][1] ];
      return strokes;
    };

    function urlParam(name) {
      var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(top.window.location.href); 
      return (results !== null) ? results[1] : undefined;
    };
    
    var $canvas = $('#drawing-canvas').sketchable({
      graphics: {
        strokeStyle: "red",
        firstPointSize: 2
      }
    });
    
    function clearStrokes() {
      $canvas.sketchable('clear');
      $('.result').empty();
    };
    
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

    function submitStrokes() {
      var $submit = $('a#send'), $latex = $('#eq-latex'), $render = $('#eq-render');
      var strokes = $canvas.sketchable('strokes');
      // Submit strokes in the required format.
      var strokes2 = transform(strokes);
      var strokes3 = strokesToScg(strokes2);
      $.ajax
      ({
          type: "POST",
          url: '/background_process_test',
          dataType: 'json',
          contentType: "application/json; charset=utf-8",
          async: false,
          //json object to sent to the authentication url
          data: JSON.stringify(strokes3),
          beforeSend: function(xhr) {
            console.log("Wait...")
          },
          finish: function (data) {
            console.log("Finish! LaTeX: " + data); 
          },

          success: function (data) {
            console.log("Sucess! LaTeX: " + data);
            console.log(typeof data)
            latex = data.replace(/ /g,'');
          }
      })
      // $.getJSON('/background_process_test',
      // function(data) {
      // //
      //   });
      // console.log(strokesToScg(strokes));
      // var postdata = { strokes: JSON.stringify(strokes) };
      // if (urlParam("train")) {
      //   postdata.label = $('#train').val();
      //   postdata.user = urlParam("user");
      // }
      // $.ajax({
      //   url: "eq.php",
      //   type: "POST",
      //   data: postdata,
      //   beforeSend: function(xhr) {
      //     $submit.hide();
      //     var loading = '<div id="loading"> \
      //                     <img class="inline" src="css/funnel.gif"/> \
      //                     <h2 class="inline">Recognizing...</h2> \
      //                     <h4>This might take a while.</h4> \
      //                    </div>';
      //     $('.eq').prepend(loading);
      //     $latex.empty();
      //     $render.empty();
      //   },
      //   error: function(jqXHR, textStatus, errorThrown) {
      //     $('.eq').html('<h2>' + textStatus + '</h2><p>' + errorThrown + '</p>');
      //   },
      //   success: function(data, textStatus, jqXHR) {
      //     if (!data) {
      //       $('.eq').html('<h2>Server not available.</h2><p>Please try again later. We apologize for the inconvenience.</p>');
      //       return false;
      //     }
      //     $submit.show();
      //     $('#loading').remove();
      //     var asurl = encodeURIComponent(data);
      //     var query = '<p id="query">Search this in \
      //       <a target="_blank" href="https://www.google.es/search?q=' + asurl + '">Google</a> \
      //       or in <a target="_blank" href="https://www.wolframalpha.com/input/?i=' + asurl + '">Wolfram|Alpha</a>.';
      //     $latex.html(data + '<br/>' + query);
      //     $render.html('\\[' + data + '\\]');
      //     MathJax.Hub.Typeset();
      //   }
      // });   
    };

    $('#send_equation').on("click",function gg() {
      submitStrokes();
      latex = latex.replace(/\\\\/g, "\\");
      console.log(typeof latex)
      $('input[name="eq_first"]').val(latex);
    });

    $('#send_equation2').on("click",function hh() {
      submitStrokes();
      latex = latex.replace(/\\\\/g, "\\");
      $('input[name="eq_last"]').val(latex);
    });

    $('#send_equation3').on("click",function ii() {
      submitStrokes();
      latex = latex.replace(/\\\\/g, "\\");
      $('input[name="eq_final_1"]').val(latex);
    });

    $('#send_equation4').on("click",function jj() {
      submitStrokes();
      latex = latex.replace(/\\\\/g, "\\");
      $('input[name="eq_final_2"]').val(latex);
    });

    $('a#clear').on("click", function(e){
      e.preventDefault();
      clearStrokes();
    });
    
    $('a#send').on("click", function(e){
      e.preventDefault();
      submitStrokes();
    });
        
    $('a#undo').on("click", function(e){
      e.preventDefault();
      $canvas.sketchable('undo');
    });

    $('a#redo').on("click", function(e){
      e.preventDefault();
      $canvas.sketchable('redo');
    });
    
    if (urlParam("train")) {
      // Shortcut to clear canvas + submit strokes.
      $(document).on("keydown", function(e){
        //if (e.ctrlKey && e.which == 65) { // This can be exhausting.
        if (e.which == 45 || e.which == 96) { // Better be pressing a single key, e.g. INS.
          e.preventDefault();
          submitStrokes();
          clearStrokes();
        }
      });
    }
    
    // Render LaTeX math expressions on page load.
    MathJax.Hub.Config({ showMathMenu:false });
    MathJax.Hub.Typeset();
});
