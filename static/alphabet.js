var conn;
var wheel;

function connect(user) {
    conn = new SockJS('http://' + window.location.host + '/alphabet');
    console.log('Connecting...');
    conn.onopen = function () {
        console.log('Connected.');
        conn.send('auth|' + user);
    };
    conn.onmessage = function (e) {
        console.log('Received: ' + e.data);
        if(typeof(e.data) === 'object') {
            wheel = new LettersWheel(e.data);
            drawLetters();
        }
    };
    conn.onclose = function () {
        console.log('Disconnected.');
        conn = null;
    };
}

var points;
var x, y, r;
var stage;
var pointsLabel;
var middleLetter;
var pool;

function init(user, score) {
    connect(user);
    x = 250;
    y = 250;
    r = 150;
    points = score;
    stage = new createjs.Stage("game");
    pool = new LettersPool();

    middleLetter = new createjs.Text("", "40px Arimo", "#dd0000");
    middleLetter.x = x;
    middleLetter.y = y;
    middleLetter.textBaseline = "middle";
    middleLetter.textAlign = "center";
    stage.addChild(middleLetter);

    pointsLabel = new createjs.Text("score: "+points, "20px Arimo", "#000000");
    pointsLabel.x = 10;
    pointsLabel.y = 20;
    stage.addChild(pointsLabel);

    createjs.Ticker.addEventListener("tick", function() {
        stage.update();
    });
}

function drawLetters() {
    for(var i = 0; i < wheel.getLength(); i++) {
        var letter = pool.newLetter(wheel.getLetter(i), "Violet", 30);
        letter.setPosition(x + Math.sin(Math.PI*2/wheel.getLength()*i)*r, y - Math.cos(Math.PI*2/wheel.getLength()*i)*r);
        stage.addChild(letter.container);
    }

    wheel.chooseNextAnswer();
    middleLetter.text = wheel.getCurrentLetterName();
}

function chooseLetter(letter) {
    if(letter.text === wheel.getCurrentLetter()) {
        points += 10;
        pointsLabel.text = "score: "+points;
        createjs.Tween.get(letter.container, {override: true}).to({x: x, y: y, alpha: 0}, 500, createjs.Ease.cubicIn).call(function() {
            stage.removeChild(letter.container);
        });
        pool.removeLetter(letter);
        if(wheel.chooseNextAnswer())
            middleLetter.text = wheel.getCurrentLetterName();
        else {
            middleLetter.text = "Excellent!";
            setTimeout(function() {
                conn.send('score|' + points);
            }, 1000);
        }
    }
    else {
        points -= 1;
        if(points < 0)
            points = 0;
        pointsLabel.text = "score: "+points;
    }
}

// LETTERSWHEEL CLASS

var LettersWheel = function(alphabet) {
    this.alphabet = alphabet;

    this.iterator = (function(array) {
        var indices = [];
        for(var i = 0; i < array.length; i++) {
            indices[i] = i;
        }
        shuffle(indices);
        var index = 0;

        return {
            getNext: function() {
                return array[indices[index++]];
            },
            hasNext: function() {
                return index < array.length;
            }
        }
    })(alphabet);
};

LettersWheel.prototype.getLength = function() {
    return this.alphabet.length;
};

LettersWheel.prototype.getLetter = function(n) {
    return this.alphabet[n][1];
};

LettersWheel.prototype.getLetterName = function(n) {
    return this.alphabet[n][0];
};

LettersWheel.prototype.chooseNextAnswer = function() {
    if(this.iterator.hasNext()) {
        this.current = this.iterator.getNext();
        return true;
    }
    return false;
};

LettersWheel.prototype.getCurrentLetter = function() {
    return this.current[1];
};

LettersWheel.prototype.getCurrentLetterName = function() {
    return this.current[0];
};

function shuffle(a) {
    var j, x, i;
    for (i = a.length; i; i -= 1) {
        j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }
}

// LETTER CLASS

var Letter = function(text, color, radius) {
    this.text = text;
    this.color = color;
    this.radius = radius;
};

Letter.prototype.construct = function() {
    if(this.container === undefined) {
        this.container = new createjs.Container();
        this.circle = new createjs.Shape();
        this.circle.graphics.beginFill(this.color).beginStroke('Black').drawCircle(0, 0, this.radius);
        this.container.addChild(this.circle);
        this.letter = new createjs.Text(this.text, "30px Arimo", "#000000");
        this.letter.textBaseline = "middle";
        this.letter.textAlign = "center";
        this.container.addChild(this.letter);
        var letter = this;
        this.container.addEventListener('click', function(e) {
            chooseLetter(letter);
        });
    }
};

Letter.prototype.setPosition = function(x, y) {
    this.container.x = x;
    this.container.y = y;
};

Letter.prototype.setColor = function(color) {
    this.color = color;
    this.container.alpha = 1.0;
    this.redraw();
};

Letter.prototype.setRadius = function(radius) {
    this.radius = radius;
    this.redraw();
};

Letter.prototype.setText = function(text) {
    this.text = text;
    this.letter.text = text;
};

Letter.prototype.redraw = function() {
    this.circle.graphics.clear().beginStroke('Black').beginFill(this.color).drawCircle(0, 0, this.radius);
};

// LETTERSPOOL CLASS

var LettersPool = function() {
    this.active = [];
    this.passive = [];
};

LettersPool.prototype.newLetter = function(text, color, radius) {
    var letter;
    if(this.passive.length > 0) {
        letter = this.passive.pop();
        letter.setText(text);
        letter.setColor(color);
        letter.setRadius(radius);
        this.active.push(letter);
    }
    else {
        letter = new Letter(text, color, radius);
        letter.construct();
        this.active.push(letter);
    }
    return letter;
};

LettersPool.prototype.removeLetter = function(letter) {
    var index = this.active.indexOf(letter);
    if(index > -1) {
        this.active.splice(index, 1);
        this.passive.push(letter);
    }
};