var input = document.getElementById("url-input");
var state = false;

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
        alert("Scraping " + input.value);
    }
})

var noOfButtons = 5;
var buttonsText = [];
var displayArea = document.getElementById("display-area");

for (var i = 0; i < noOfButtons; i++) {
    var newButton = document.createElement("div");
    newButton.setAttribute("class", "button");
    
    /*Button Text*/

    displayArea.appendChild(newButton);
}