let textarea = document.getElementById("area")
let cont = document.getElementById("main-cont")
let line = document.getElementById("bg")
let title = document.getElementById("title")
let onfocused = false

textarea.onclick = () => {
    textarea.innerHTML = ""
    onfocused = true
    clearQueue()
}
textarea.onkeydown = () => {
    textarea.innerHTML = ""
    onfocused = true
    clearQueue()
}
let event = new Event('focusout');
textarea.dispatchEvent(event);

textarea.addEventListener('focusout', function (eventObj) {
    onfocused = false
});
let clearflag = false

let buffer = 0
let intervals = []

function backgroundText(size, time, border, poem, fontSize) {
    let contWidth = cont.offsetWidth
    let maxWordHeight = Math.floor(1.5 * fontSize)
    let maxWordWidth = (window.innerWidth - contWidth) / 2 - border * 2
    console.log(maxWordWidth)
    let height = Math.floor((window.innerHeight - border) / maxWordHeight)
    let words = []
    let freeCells = []
    let id = 0
    for (let i = 1; i <= size; i++) {
        words[i - 1] = document.createElement('div');
        words[i - 1].className = "word";
        document.body.append(words[i - 1]);
    }
    for (let j = 0; j < height; j++)
        if (border < maxWordHeight * (j + 1) &&
            2 * border + maxWordHeight * (j + 1) < window.innerHeight) {
            freeCells.push({x: 0, y: j * maxWordHeight})
            freeCells.push({x: window.innerWidth - border - maxWordWidth, y: j * maxWordHeight})
        }

    function setRandomXY(elem) {
        if (id + 1 > poem.length) {
            clearQueue()
            clearflag = true
            return
        }
        let text = poem[id]
        elem.innerHTML = text;
        let midWordWidth = textLength(text, fontSize)
        id++
        let index = Math.floor(Math.random() * freeCells.length)
        let cell = freeCells[index]
        freeCells.splice(index, 1)
        elem.style.top = (border + cell.y + Math.floor(Math.random() * (maxWordHeight - fontSize))) + "px"
        elem.style.left = (border + cell.x + Math.floor(Math.random() * (maxWordWidth - midWordWidth))) + "px"
        setTimeout(() => typeWriter(text, time / 2, 0), time / 4)
        elem.style.color = "white"

        setTimeout(() => {
            elem.style.color = "#77BEFF"
        }, time / 2)
        setTimeout(() =>
            freeCells.push(cell), time)

    }

    setTimeout(() => setRandomXY(words[0]), 1000)
    for (let i = 0; i < size; i++) {
        setTimeout(() => intervals.push(setInterval(() => setRandomXY(words[i]), time)), (time / size) * i)
    }
}

function textLength(phrase, fontsize) {
    let ml = 0.5105263157894737;
    return Math.floor(phrase.length * fontsize * ml);
}


function clearQueue() {
    intervals.forEach(ent => clearInterval(ent))
}

function typeWriter(phrase, time, i) {
    if (!onfocused) {
        let speed = Math.min(50, Math.floor(time / 2 / phrase.length));
        if (i < phrase.length) {
            textarea.innerHTML += phrase.charAt(i);
            textarea.selectionStart = buffer + i + 1;
            i++;
            setTimeout(() => typeWriter(phrase, time, i), speed);
        } else {
            document.getElementById("area").innerHTML += "\n"
            buffer += i + 1;
            textarea.selectionStart = buffer;
        }
    }
}

autoPoem()

setInterval(() => {
    console.log(textarea.innerHTML, onfocused)
    if (clearflag) {
        clearflag = false
        setTimeout(slowClear, 1000)
    }
    if (textarea.innerHTML === '' && !onfocused)
        autoPoem()
}, 5000)

function autoPoem() {
    clearQueue()
    slowClear(2)
    getRandomPoem()
}

function slowClear(time) {
    if (textarea.innerHTML !== '') {
        setTimeout(() => {
            textarea.innerHTML = textarea.innerHTML.substring(0, textarea.innerHTML.length - 1)
            slowClear(time, 0);
        }, time)
    }
}

function uploadPoem() {
    clearQueue()
    fetch('http://127.0.0.1:2080/main/uploadPoem', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify([textarea.value])
    })
        .then(response => response.json())
        .then(response => {
            console.log(JSON.stringify(response))
            cont.style.transform = "translate(0, 94%)"
            line.classList.add('trigger')
            line.onclick = clickArrow
            clearQueue()
            drawCloud(response['data']);
        })
}

function getRandomPoem() {
    let poem = []
    fetch('http://127.0.0.1:2080/main/poem', {
        method: 'GET'
    })
        .then(response => response.json())
        .then(response => {
            console.log(response['text'])
            backgroundText(2, 4000, 100, response['text'], 25)
        })
    console.log(poem)
    return poem.text
}

function clickArrow(b = true) {
    line.classList.remove('trigger')
    cont.style.transform = "translate(0, 0%)"
    if (b)
        cleanLayout();
}

function titleSelected(name) {
    title.innerHTML = name
    setTimeout(() => clickArrow(false), 1200)
}
