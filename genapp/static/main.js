$('.submit').on('click', function () {
    submit()
})

function submit() {
    const csrftoken = getCookie('csrftoken');
    const real = $(".real").val()
    const bin = $(".bin").val()
    const rangeA = $(".rangeA").val()
    const rangeB = $(".rangeB").val()
    const precision = $(".precision").val()

    $.ajax({
        url: 'start/',
        type: 'POST',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrftoken,
            real: real,
            bin: bin,
            rangeA: rangeA,
            rangeB: rangeB,
            precision: precision,
        },
        success: function (result) {
            $(".power-response").text(result.power)
            $(".real-response").text(result.real)
            $(".bin-response").text(result.bin)
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