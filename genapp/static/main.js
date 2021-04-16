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

$('.test').click(function () {
    test();
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
                    "<td>" + result.real + "</td>" +
                    "<td>" + result.int_from_real + "</td>" +
                    "<td>" + result.binary + "</td>" +
                    "<td>" + result.int_from_bin + "</td>" +
                    "<td>" + result.real_from_int + "</td>" +
                    "<td>" + result.fx + "</td>" +
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
                    "<td>" + result.real + "</td>" +
                    "<td>" + result.fx + "</td>" +
                    "<td>" + result.gx + "</td>" +
                    "<td>" + result.px + "</td>" +
                    "<td>" + result.qx + "</td>" +
                    "<td class='border-start'>" + result.random + "</td>" +
                    "<td>" + selected[index].real + "</td>" +
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
                    "<td>" + result.real + "</td>" +
                    "<td>" + result.binary + "</td>" +
                    "<td>" + (result.is_parent === true ? result.binary : "------") + "</td>" +
                    "<td>" + (result.crossover_points != "" ? result.crossover_points : "--") + "</td>" +
                    "<td>" + (result.child_binary != null ? result.child_binary : "------") + "</td>" +
                    "<td>" + result.cross_population + "</td>" +
                    "<td>" + result.mutation_points + "</td>" +
                    "<td>" + result.mutant_population + "</td>" +
                    "<td>" + newPopulation[index].real + "</td>" +
                    "<td>" + newPopulation[index].fx + "</td>" +
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
    const elite = $('.elite option:selected').val()

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
            mutation_probability: mutationProbability,
            elite: elite
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

function test() {
    const csrftoken = getCookie('csrftoken');
    const testsNumber = $(".testsNumber").val()
    const precision = $(".testPrecision").val()

    $(".test").attr("disabled", "disabled");

    $(".tests-results").html('<tr><td colspan="7"><div class="d-flex justify-content-center"><div class="spinner-border" role="status"></div></div></td></tr>')
    
    $.ajax({
        url: location.origin + '/test/',
        type: 'POST',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrftoken,
            tests_number: testsNumber,
            precision: precision
        },
        success: function (results) {
            let html = '';
            JSON.parse(results.test).forEach(function (result, index) {
                let elem =
                    "<tr> " +
                    "<th scope='row'>" + (index + 1) + "</th>" +
                    "<td>" + result.population_size + "</td>" +
                    "<td>" + result.generations_number + "</td>" +
                    "<td>" + result.crossover_probability + "</td>" +
                    "<td>" + result.mutation_probability + "</td>" +
                    "<td>" + result.fmax + "</td>" +
                    "<td>" + result.favg + "</td>" +
                    "</tr>"
                html += elem;
            });

            $(".tests-results").html(html);
            $(".test").removeAttr("disabled");
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
        position: 'right',
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