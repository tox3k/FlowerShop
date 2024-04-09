function addCart(id){
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/add-cart/"+id)
    xhr.send()
}

async function removeCart(id){
    let request = '/remove-cart/'+id;
    let xhr = new XMLHttpRequest();
    xhr.open('GET', request);
    let promise = new Promise((resolve, reject) => {
        setTimeout(() => resolve(""), 100)
      });
      
    xhr.send();
    await promise;
    location.reload(true);
}

async function increaseCount(id){
    let request = '/add-cart/'+id;
    let xhr = new XMLHttpRequest();
    xhr.open('GET', request);
    let promise = new Promise((resolve, reject) => {
        setTimeout(() => resolve(""), 100)
      });
      
    xhr.send();
    await promise;
    location.reload(true);
}

async function decreaseCount(id){
    let request = '/decrease-count/'+id;
    let xhr = new XMLHttpRequest();
    xhr.open('GET', request);
    let promise = new Promise((resolve, reject) => {
        setTimeout(() => resolve(""), 100)
      });
      
    xhr.send();
    await promise;
    console.log('REMOVED')
    location.reload(true);
}

function CardTextResize() {
    let cards = document.querySelectorAll('.card');
    cards.forEach((card) => {
        let h2 = card.querySelector('.card-name-box h2');
        let h2Box = card.querySelector('.card-name-box')
        let description = card.querySelector('.description');
        let descriptionBox = card.querySelector(".description-box");

        let h2Text = h2.innerText;
        let containsLongWord = false;
        h2.style.wordBreak = "normal";
        for (let subStr of h2Text.split(' ')){
            
            if (subStr.length > 11){
                h2.style.wordBreak="break-all";
                containsLongWord = true
                console.log(subStr + ' ' + containsLongWord)
                break;
            }
        }
        if (containsLongWord)
            h2.style.fontSize = Math.ceil(Math.sqrt(h2Box.clientWidth * h2Box.clientHeight / h2Text.length) * 0.8) + "px";
        else
            h2.style.fontSize = Math.ceil(Math.sqrt(h2Box.clientWidth * h2Box.clientHeight / h2Text.length) * 0.9) + "px";

        let descriptionText = description.innerText;
        let longWord = false;
        description.style.wordBreak="normal";
        for (let subStr of descriptionText.split(' ')){
            
            if (subStr.length > 20){
                h2.style.wordBreak="break-all";
                longWord = true
                console.log(subStr + ' ' + containsLongWord)
                break;
            }
        }
        let descFontSize = Math.ceil(Math.sqrt(descriptionBox.clientWidth * descriptionBox.clientHeight / descriptionText.length) * 0.8);
        if (descFontSize > 30)
            descFontSize = 30;
        description.style.fontSize = descFontSize + "px";
        
    })  
}
window.onload = CardTextResize
