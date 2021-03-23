$('.start').on('click', function () {
    start();
})

$('.selection').on('click', function () {
    selection();
})

function start() {
    const csrftoken = getCookie('csrftoken');
    const rangeA = $(".rangeA").val()
    const rangeB = $(".rangeB").val()
    const precision = $(".precision").val()
    const population = $(".population").val()

    $.ajax({
        url: location.origin + '/start/',
        type: 'POST',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrftoken,
            rangeA: rangeA,
            rangeB: rangeB,
            precision: precision,
            population: population
        },
        success: function (results) {
            $(".power").val(results.power)

            let html = '';

            JSON.parse(results.individuals).forEach(function (result, index) {
                let elem = 
                    "<tr> " +
                        "<th scope='row'>" + (index + 1) + "</th>" +
                        "<td>" + result.fields.real + "</td>" + 
                        "<td>" + result.fields.int_from_real + "</td>" + 
                        "<td>" + result.fields.binary + "</td>" + 
                        "<td>" + result.fields.int_from_bin + "</td>" + 
                        "<td>" + result.fields.real_from_int + "</td>" + 
                        "<td>" + result.fields.fx + "</td>" + 
                    "</tr>"

                html += elem;
            })

            $(".results").html(html);
        }
    });
}

function selection(){
    const csrftoken = getCookie('csrftoken');
    const rangeA = $(".rangeA").val()
    const rangeB = $(".rangeB").val()
    const precision = $(".precision").val()
    const population = $(".population").val()

    $.ajax({
        url: location.origin + '/selection/',
        type: 'POST',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrftoken,
            rangeA: rangeA,
            rangeB: rangeB,
            precision: precision,
            population: population
        },
        success: function (results) {
            let html = '';
            let selected = JSON.parse(results.selected_individuals)

            JSON.parse(results.individuals).forEach(function (result, index) {
                let elem = 
                    "<tr> " +
                        "<th scope='row'>" + (index + 1) + "</th>" +
                        "<td>" + result.fields.real + "</td>" + 
                        "<td>" + result.fields.fx + "</td>" + 
                        "<td>" + result.fields.gx + "</td>" + 
                        "<td>" + result.fields.px + "</td>" + 
                        "<td>" + result.fields.qx + "</td>" + 
                        "<td class='border-start'>" + results.randoms[index] + "</td>" + 
                        "<td>" + selected[index].fields.real + "</td>" + 
                    "</tr>"

                html += elem;
            })

            $(".results").html(html);
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