$('.start').click(function () {
    start();
})

$('.selection').click(function () {
    selection();
})

$('.crossover').click(function () {
    crossover();
})

$('.evolution').click(function () {
    evolution();
})

chart = drawChart(); 

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
            range_a: rangeA,
            range_b: rangeB,
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

function selection() {
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
            range_a: rangeA,
            range_b: rangeB,
            precision: precision,
            population: population
        },
        success: function (results) {
            let html = '';
            let selected = JSON.parse(results.selected_individuals);

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

function crossover() {
    const csrftoken = getCookie('csrftoken');
    const rangeA = $(".rangeA").val()
    const rangeB = $(".rangeB").val()
    const precision = $(".precision").val()
    const population = $(".population").val()
    const crossoverProbability = $(".crossoverProbability").val()
    const mutationProbability = $(".mutationProbability").val()

    $.ajax({
        url: location.origin + '/crossover/',
        type: 'POST',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrftoken,
            range_a: rangeA,
            range_b: rangeB,
            precision: precision,
            population: population,
            crossover_probability: crossoverProbability,
            mutation_probability: mutationProbability
        },
        success: function (results) {
            let html = '';
            let newPopulation = JSON.parse(results.new_population);

            JSON.parse(results.individuals).forEach(function (result, index) {
                let elem =
                    "<tr> " +
                    "<th scope='row'>" + (index + 1) + "</th>" +
                    "<td>" + result.fields.real + "</td>" +
                    "<td>" + result.fields.binary + "</td>" +
                    "<td>" + (result.fields.is_parent === true ? result.fields.binary : "------") + "</td>" +
                    "<td>" + (result.fields.crossover_points != "" ? result.fields.crossover_points : "--") + "</td>" +
                    "<td>" + (result.fields.child_binary != "" ? result.fields.child_binary : "------") + "</td>" +
                    "<td>" + result.fields.cross_population + "</td>" +
                    "<td>" + result.fields.mutation_points + "</td>" +
                    "<td>" + result.fields.mutant_population + "</td>" +
                    "<td>" + newPopulation[index].fields.real + "</td>" +
                    "<td>" + newPopulation[index].fields.fx + "</td>" +
                    "</tr>"

                html += elem;
            })

            $(".results").html(html);
        }
    });
}

function evolution() {
    const csrftoken = getCookie('csrftoken');
    const rangeA = $(".rangeA").val()
    const rangeB = $(".rangeB").val()
    const precision = $(".precision").val()
    const population = $(".population").val()
    const generations = $(".generations").val()
    const crossoverProbability = $(".crossoverProbability").val()
    const mutationProbability = $(".mutationProbability").val()

    $(".evolution").attr("disabled", "disabled");
    
    $.ajax({
        url: location.origin + '/evolution/',
        type: 'POST',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrftoken,
            range_a: rangeA,
            range_b: rangeB,
            precision: precision,
            population: population,
            generations: generations,
            crossover_probability: crossoverProbability,
            mutation_probability: mutationProbability
        },
        success: function (results) {
            let html = '';

            results.last_generation.forEach(function (result, index) {
                let elem =
                    "<tr> " +
                    "<th scope='row'>" + (index + 1) + "</th>" +
                    "<td>" + result.real + "</td>" +
                    "<td>" + result.bin + "</td>" +
                    "<td>" + result.fx + "</td>" +
                    "<td>" + result.percent + "</td>" +
                    "</tr>"
                html += elem;
            });

            updateChart(chart, generations, results.data_for_chart);
            $(".results").html(html);
            $(".evolution").removeAttr("disabled");
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

function drawChart() {
    var ctx = document.getElementById('myChart');

    const config = {
        type: 'line',
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    font: {
                        size: 20
                    },
                    display: true,
                    text: 'Wyniki działania algorytmu'
                },
            },
            interaction: {
                intersect: false,
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Wartość'
                    },
                    suggestedMin: -1.5,
                    suggestedMax: 2
                }
            }
        },
    };

    return new Chart(ctx, config);
}

function updateChart(chart, generations, generationsData) {    
    const DATA_COUNT = generations;
    const labels = [];

    for (let i = 1; i <= DATA_COUNT; ++i) {
        labels.push(i.toString());
    }

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'fmax',
                data: generationsData.map(function(data) {return data.fmax;}),
                borderColor: '#dc3545',
                fill: false,
                cubicInterpolationMode: 'monotone',
                tension: 0.4
            },
            {
                label: 'favg',
                data: generationsData.map(function(data) {return data.favg;}),
                borderColor: '#28a745',
                fill: false,
                cubicInterpolationMode: 'monotone',
                tension: 0.4
            },
            {
                label: 'fmin',
                data: generationsData.map(function(data) {return data.fmin;}),
                borderColor: '#007bff',
                fill: false,
                cubicInterpolationMode: 'monotone',
                tension: 0.4
            },
        ]
    };

    chart.data = data;
    chart.update();
}