var search_button = document.getElementById('search_button');
var search_textbox = document.getElementById('search_text');

var BASE_URL = "http://127.0.0.1:5000";

search_button.addEventListener('click', ()=>{
    let value = search_textbox.value;
    let url = BASE_URL + "/paper/search?query=" + String(value);
    fetch(url)
    .then(text => text.json())
    .then(data => {
        parent = document.getElementById("view-container")
        parent.innerHTML = ""
        for (let i = 0; i < data.length; i++) {
            content = `
            <div class="col-md-12">
                <div class="feature-item">
                    <div class="icon">
                        <img src="assets/images/feature-01.png" alt="">
                    </div>
                <h4>${data[i]["title"]}</h4>
                <h4>CONFERENCE : ${data[i]["conference"]["abbr"]}</h4>
                <h4>RANK : ${data[i]["conference"]["rank"]}</h4>
                </div>
            </div>`
            parent.innerHTML = parent.innerHTML + content
        }
    })
});