function addCart(id){
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/add-cart/"+id)
    xhr.send()
}

function addNewProduct(){
    let form = document.querySelector('.add_products form');
    let name = form.querySelector('.name');
    let category = form.querySelector('.category_list');
    let flowerCategory = form.querySelector('.flower_category');
    let description = form.querySelector('.description');
    let stock = form.querySelector('.stock');
    let is_actual = form.querySelector('.is_actual');
    let price = form.querySelector('.price');
    let photo = form.querySelector('.photo');

    var data = {
        name: name.value,
        category: category.value,
        flowerCategory: flowerCategory.value,
        description: description.value,
        stock: stock.value,
        is_actual: is_actual.value,
        price: price.value,
        photo: photo.value

      };
      
      var boundary = String(Math.random()).slice(2);
      var boundaryMiddle = '--' + boundary + '\r\n';
      var boundaryLast = '--' + boundary + '--\r\n'
      
      var body = ['\r\n'];
      for (var key in data) {
        // добавление поля
        body.push('Content-Disposition: form-data; name="' + key + '"\r\n\r\n' + data[key] + '\r\n');
      }
      
      body = body.join(boundaryMiddle) + boundaryLast;
      

    let xhr = XMLHttpRequest();
    xhr.open("POST")

    // console.log(name.value)
    // console.log(category.value)
    // console.log(flowerCategory)
    // console.log(description.value)
    // console.log(stock.value)
    // console.log(is_actual.value)
    // console.log(price.value)
    // console.log(photo.value)

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
        if (h2Text.split(' ').length < 3){
            if (h2Text.split(' ').length == 1)
                h2.style.fontSize = Math.ceil(h2Box.clientWidth / h2Text.length * 1.2) + "px";
            else{
                h2.style.fontSize = Math.ceil(h2Box.clientWidth * 2 / h2Text.length) + "px";
            }
        }
        else{
            for (let subStr of h2Text.split(' ')){
            
            if (subStr.length > 5){
                h2.style.wordBreak="break-all";
                containsLongWord = true
                console.log(subStr + ' ' + containsLongWord)
                break;
            }
            if (containsLongWord)
            h2.style.fontSize = Math.ceil(Math.sqrt(h2Box.clientWidth * h2Box.clientHeight / h2Text.length) * 0.8) + "px";
        else
            h2.style.fontSize = Math.ceil(Math.sqrt(h2Box.clientWidth * h2Box.clientHeight / h2Text.length) * 0.9) + "px";
        }
        }
        
        

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
