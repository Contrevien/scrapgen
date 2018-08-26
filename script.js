var input = document.getElementById("url-input");
var state = false;
var isLoading = false;

input.oninput = () => {
    var url = /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/
    if (url.test(input.value)===false){
        document.getElementById("status").style.visibility = "visible";
        state = false;
    }
    else {
        document.getElementById("status").style.visibility = "hidden";
        state = true;
    }
}

input.addEventListener("keydown", (e) => {
    if (e.keyCode === 13 && state) {
        isLoading = true;
        document.getElementById("loader-container").style.display = "flex";
    }
})

var buttonsText = [
    {
        "div":[
            "id=\"main\"",
        ]
    },
    {
        "h1":[
            "id=\"header\"",
            "My website"
        ]
    },
    {
        "img":[
            "src=\"somewhere.png\"",
            "alt=\"Logo\""
        ]
    },
    {
        "input":[
            "type=\"text\"",
            "placeholder=\"Enter Name\"",
        ]
    },
    {
        "p":[
            "id=\"para-1\"",
            "class=\"site-text\"",
            "how is the weather so good today and some garbage text must go here!"
        ]
    }
];

var displayArea = document.getElementById("display-area");

for (var i = 0; i < buttonsText.length; i++) {
    var newButton = document.createElement("div");
    newButton.setAttribute("class", "button");
    
    var buttonHead = document.createElement("h2");
    buttonHead.setAttribute("class", "button-head");
    buttonHead.innerHTML = Object.keys(buttonsText[i]);
    newButton.appendChild(buttonHead);

    var buttonParaCon = document.createElement("div");
    buttonParaCon.setAttribute("class","button-para-container");
    for (var j in buttonsText[i][Object.keys(buttonsText[i])]){
        var buttonPara = document.createElement("p");
        buttonPara.setAttribute("class", "button-para");
        buttonPara.innerHTML = buttonsText[i][Object.keys(buttonsText[i])][j].slice(0,35);
        buttonParaCon.appendChild(buttonPara);
    }
    newButton.appendChild(buttonParaCon);
    displayArea.appendChild(newButton);
    newButton.addEventListener("click", select)
}

function select(e) {
    var target = null;
    if(e.target.parentNode.className === "button"||e.target.parentNode.className === "button selected"){
        target = e.target.parentNode;
    }
    else if(e.target.parentNode.parentNode.className === "button"||e.target.parentNode.parentNode.className === "button selected"){
        target = e.target.parentNode.parentNode;
    }
    else if(e.target.className === "button"||e.target.className === "button selected"){
        target = e.target;
    }
    target.classList.toggle("selected");
}

document.getElementById("reset").addEventListener("click", () => {
    var buttons = document.querySelectorAll(".button");
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove("selected");
    }
})