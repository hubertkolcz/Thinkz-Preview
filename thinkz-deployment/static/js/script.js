var hand;
let link;
var answer;
var handy;

function twoSolutions() {
    if (document.getElementById('2solutions').checked) {
        document.getElementById('1stSol').style.display = 'block';
        document.getElementById('2ndSol').style.display = 'block';
    }
}

function oneSolution() {
    if (document.getElementById('1solution').checked) {
        document.getElementById('1stSol').style.display = 'block';
        document.getElementById('2ndSol').style.display = 'none';
    }
}

function zeroSolution() {
    if (document.getElementById('0solutions').checked) {
        document.getElementById('2ndSol').style.display = 'none';
        document.getElementById('1stSol').style.display = 'none';
    }
}

function infinitySolution() {
    if (document.getElementById('infinity').checked) {
        document.getElementById('2ndSol').style.display = 'none';
        document.getElementById('1stSol').style.display = 'none';
    }
}

const url = 'http://0.0.0.0:9292/equation';
const data = {"strokes": "SCG_INK\\n2\\n2\\n270 1372\\n466 1549\\n2\\n437 1393\\n261 1546\\n"};

var xhr = new XMLHttpRequest();
xhr.open("POST", url, true);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.send(JSON.stringify(data));


window.onload = function () {
  hand = com.wiris.js.JsHand.newInstance();
  hand.insertInto(document.getElementById('handContainer'));

  hand.addHandListener({
    contentChanged: function (instance) {
      document.getElementById('result').value = hand.getMathML();
      document.getElementById('result2').innerHTML = hand.getMathML();
      // $('#result2').html(hand.getMathML());
      MathJax.Hub.Queue(["Typeset",MathJax.Hub,"result"]);
    },
    recognitionError: function (instance, msg) {
      document.getElementById('result').value = "Error: " + msg;
    },
    strokesChanged: function(instance) {}
  });
}
function f() {
    $('#equation').empty();
    $(hand.getMathML()).appendTo($('#equation'));
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    handy = hand.getMathML();
 }

function g() {
    $('#equation2').empty();
    var answer;
    var xhr = new XMLHttpRequest;
    link = 'https://www.wiris.net/demo/editor/mathml2latex?mml=' + handy;
    link2 = 'https://www.wiris.net/demo/editor/mathml2latex?mml=%3Cmath%3E%3Cmn%3E2%3C/mn%3E%3Cmo%3E-%3C/mo%3E%3Cmi%3Ex%3C/mi%3E%3C/math%3E';
    xhr.open('GET', link, true);
    console.log('OPENED: ', xhr.status);

    xhr.send();
    xhr.onload = function () {
        console.log('DONE: ', xhr.status);
        if (this.status === 200) {
            console.log(this.responseText);
            answer = this.responseText;
            $("<strong>" + answer + "</strong>").appendTo($('#equation2'));
            $('input[name="eq_first"]').val(answer);
        }
    }
}

function h() {
    $('#equation2').empty();
    var answer;
    var xhr = new XMLHttpRequest;
    link = 'https://www.wiris.net/demo/editor/mathml2latex?mml=' + handy;
    link2 = 'https://www.wiris.net/demo/editor/mathml2latex?mml=%3Cmath%3E%3Cmn%3E2%3C/mn%3E%3Cmo%3E-%3C/mo%3E%3Cmi%3Ex%3C/mi%3E%3C/math%3E';
    xhr.open('GET', link, true);
    console.log('OPENED: ', xhr.status);

    xhr.send();
    xhr.onload = function () {
        console.log('DONE: ', xhr.status);
        if (this.status === 200) {
            console.log(this.responseText);
            answer = this.responseText;
            $("<strong>" + answer + "</strong>").appendTo($('#equation2'));
            $('input[name="eq_last"]').val(answer);
        }
    }
}

function i() {
    $('#equation2').empty();
    var answer;
    var xhr = new XMLHttpRequest;
    link = 'https://www.wiris.net/demo/editor/mathml2latex?mml=' + handy;
    link2 = 'https://www.wiris.net/demo/editor/mathml2latex?mml=%3Cmath%3E%3Cmn%3E2%3C/mn%3E%3Cmo%3E-%3C/mo%3E%3Cmi%3Ex%3C/mi%3E%3C/math%3E';
    xhr.open('GET', link, true);
    console.log('OPENED: ', xhr.status);

    xhr.send();
    xhr.onload = function () {
        console.log('DONE: ', xhr.status);
        if (this.status === 200) {
            console.log(this.responseText);
            answer = this.responseText;
            $("<strong>" + answer + "</strong>").appendTo($('#equation2'));
            $('input[name="eq_final_1"]').val(answer);
        }
    }
}

function j() {
    $('#equation2').empty();
    var answer;
    var xhr = new XMLHttpRequest;
    link = 'https://www.wiris.net/demo/editor/mathml2latex?mml=' + handy;
    link2 = 'https://www.wiris.net/demo/editor/mathml2latex?mml=%3Cmath%3E%3Cmn%3E2%3C/mn%3E%3Cmo%3E-%3C/mo%3E%3Cmi%3Ex%3C/mi%3E%3C/math%3E';
    xhr.open('GET', link, true);
    console.log('OPENED: ', xhr.status);

    xhr.send();
    xhr.onload = function () {
        console.log('DONE: ', xhr.status);
        if (this.status === 200) {
            console.log(this.responseText);
            answer = this.responseText;
            $("<strong>" + answer + "</strong>").appendTo($('#equation2'));
            $('input[name="eq_final_2"]').val(answer);
        }
    }
}


var counter = 1;
var limit = 3;

function addInput(divName){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "Entry " + (counter + 1) + " <br><input type='text' name='myInputs[]'>";
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     }
}
//<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><msup><mfenced><mfrac><msup><mn>4</mn><mn>8</mn></msup><mn>4</mn></mfrac></mfenced><mn>2</mn></msup><mrow><mn>4</mn><mi>x</mi><mo>+</mo><mi>y</mi></mrow></mfrac><mo>=</mo><mi>z</mi></math>