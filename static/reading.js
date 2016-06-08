var text;
var speed = 5;

function connect(user) {
    conn = new SockJS('http://' + window.location.host + '/reading');
    console.log('Connecting...');
    conn.onopen = function () {
        console.log('Connected.');
        conn.send('auth|' + user);
    };
    conn.onmessage = function (e) {
        console.log('Received: ' + e.data);
        if(typeof(e.data) === "string") {
            var data = e.data.split("|", 2);
            console.log(data);
            $('.results').hide();
            $('form').hide();
            $('#reading-text').show();
            $(".welcome").text(data[0]);
            $("#reading-text").text(data[1]);
            $("#reading-text").textillate({ in: { effect: 'fadeInRight', delay: speed }, out: { effect: 'fadeOutLeft', delay: speed } });
            setTimeout(function() {
                $("#reading-text").textillate('out');
            }, 4000);
        }
        else if(typeof(e.data) === "object") {
            var form = $('form');
            form.text('');
            console.log(e.data);
            var questions = e.data;
            for(var i = 0; i < questions.length; i++) {
                form.append('<span class="question">' + (i+1) + ". " + questions[i].question+'</span><br>');
                for(var j = 0; j < questions[i].option.length; j++)
                    form.append('<input type="radio" id="'+i+"-"+j+'" class="answer" value="' + j + '" name="' + i + '" /><label for="'+i+"-"+j+'">'+ questions[i].option[j] + "</label><br>");
            }
            form.append('<button class="send-button">Send your answers</button>');
            $(".send-button").on('click', function(event) {
                event.preventDefault();
                var values = {};
                $.each(form.serializeArray(), function(i, field) {
                    values[field.name] = field.value;
                });
                conn.send('answer|' + JSON.stringify(values));
            });

        }
        else {
            $('form').hide();
            $('.results').show();
            $('.score').text(e.data + "/100");
        }
    };
    conn.onclose = function () {
        console.log('Disconnected.');
        conn = null;
    };
}

$(function() {
    $('.try-again').on('click', function() {
        location.reload();
    });
    $('#reading-text').on('outAnimationEnd.tlt', function () {
        $('#reading-text').hide();
        $('form').show();
    });
});

function init(user) {
    connect(user);
}