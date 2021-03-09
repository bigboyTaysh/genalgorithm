$('.submit').on('click', function () {
    submit()
})

function submit() {
    const csrftoken = getCookie('csrftoken');
    const rel = $(".rel").val()

    $.ajax({
        url: 'start/',
        type: 'POST',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrftoken,
            rel: rel,
        },
        success: function (result) {
            $(".rel-response").text(result.rel)
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}