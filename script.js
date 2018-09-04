const input = document.getElementById("url-input");
let state = false;
let isLoading = false;
const displayArea = document.getElementById("display-area");
const loader = document.getElementById("loader-container");

const pythonEditor = CodeMirror(document.getElementById("generation-area"), {
    value: "import selenium.webdriver from selenium\n",
    mode: "python"
});

let buttonsText = [
    {
        "article":[
            "id='dummy'"
        ]
    }
];

const checkURL = (url) => {
    var urlPat = /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/
    if (urlPat.test(url)===false){
        document.getElementById("status").style.visibility = "visible";
        state = false;
        return false;
    }
    else {
        document.getElementById("status").style.visibility = "hidden";
        state = true;
        return true;
    }
}

const submitURL = (e) => {
    if (e.keyCode === 13 && state) {
        isLoading = true;
        loader.style.display = "flex";
        renderButtons(buttonsText);
    }
}


input.addEventListener("input", () => checkURL(input.value));
input.addEventListener("keydown", submitURL);



function renderButtons(buttonsText){
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
        newButton.addEventListener("click", selectButton);
        if (isLoading)
            loader.style.display = "none";
    }
}


function selectButton(e) {
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

    var x = target.innerText.split('\n').join(' ');
    pythonEditor.replaceRange('\n#' + x + '\n' + 'Some random text\n', CodeMirror.Pos(pythonEditor.lastLine()));
}
