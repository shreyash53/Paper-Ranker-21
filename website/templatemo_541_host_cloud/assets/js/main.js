var search_button = document.getElementById('search_button');
var search_textbox = document.getElementById('search_text');

var BASE_URL = "http://127.0.0.1:5000";

search_button.addEventListener('click', ()=>{
    let value = search_textbox.value;
    let url = BASE_URL + "/paper/search?query=" + String(value);
    fetch(url)
    .then(text => text.json())
    .then(data => {
        console.log(data);
    })
});

