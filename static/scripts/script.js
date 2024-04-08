function addCart(id){
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/add-cart/"+id)
    xhr.send()
}
