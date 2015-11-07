var cur_page = 1;

function body_loaded(){
    // Any code we want to run when the page first loads goes here

    // We want to get the /room object but we want the one at cur_page
    get_page(cur_page);
}

function left_click() {
    cur_page = cur_page + 1;

    if (cur_page > 8) {
        cur_page = 1;
    }

    get_page(cur_page);
}

function right_click() {
    cur_page = cur_page + 1;

    if (cur_page < 0) {
        cur_page = 8;
    }

    get_page(cur_page);
}

function get_page(index) {
  $ajax({
    url: '/room/' + index,
    success: my_success_function
  })
}

// Whenever we get a successful call to the server (from AJAX) we will return here. We need to apply the data we have been returned here.
function my_success_function(data) {
    console.log(data)
    document.getElementById('main_image').src = data.image;
    document.getElementById('text_body').innerHTML = data.description;
    document.getElementById('heading').innerHTML = data.name;
}
