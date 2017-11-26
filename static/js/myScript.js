function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var slider_flag = false;

$(document).ready(function() {
    $("#network-add-slider").bootstrapSlider();
    $('#learning-speed').slider({
        step: 1,
        tooltip: 'always',
        tooltip_position: 'bottom'
    });
    $('#learning-speed-add').slider({
        step: 1,
        tooltip: 'always',
        tooltip_position: 'bottom'
    });
});

$('#result').css({
    width: 28 * 20,
    height: 28 * 20
})

var pad = new Sketchpad({
    element: '#pad',
    width: 28 * 20,
    height: 28 * 20
});

pad.penSize = 20;
pad.color = 'black';

$('#undo').click(function() {
    pad.undo();
});

$('#redo').click(function() {
    pad.redo();
});

function draw_prediction(arr) {
    arr.forEach(function(inner_array) {
        inner_array.forEach(function(item, i) {
            var value = parseInt(item * 100);
            var myclass = "progress-bar progress-bar-striped progress-bar-success active";
            if (66 >= value && value > 33) {
                myclass = "progress-bar progress-bar-striped progress-bar-warning active";
            }
            if (33 >= value) {
                myclass = "progress-bar progress-bar-striped progress-bar-danger active";
            }
            $('#progress-' + i).closest('div.row').attr("data-sort", value);
            $('#progress-' + i).prop("class", myclass);
            $('#progress-' + i).css('width', value + '%');
            $('#progress-' + i).text(value + '%');
        })
    })
    setTimeout(function() {
        var $container = $('#result');
        $container.find('.row').sort(function(a, b) {
            return +b.getAttribute('data-sort') - +a.getAttribute('data-sort');
        }).appendTo($container);
    }, 600)
}

$('#recogniseSubmit').click(function() {
    document.getElementById('pad').toBlob(function(e) {
        var data = new FormData();
        data.append('digitPhoto', e, 'image.png');
        deferred = $.ajax({
            type: 'POST',
            processData: false,
            contentType: false,
            url: 'api/recognizeDigit',
            data: data
        });
        deferred.done(function(response) {
            if (!response.ok) {
                console.log(response.error);
            } else {
                draw_prediction(response.values);
            }
        });
        deferred.fail(function() {
            console.log('Не удается распознать! Сервер недоступен');
        });
    });
});

// пример апи как слать фотку цифры на обучение и эту самую цифру

$('#recogniseAdd').click(function() {
    $('#network-add-modal').modal('show');
    if (!slider_flag) setTimeout(function() {
        $("#network-add-slider").bootstrapSlider('refresh');
        slider_flag = true;
    }, 500)
});

$('#recognise-add-ok').click(function() {
    document.getElementById('pad').toBlob(function(e) {
        var data = new FormData();
        data.append('digitPhoto', e, 'image.png');
        data.append('value', $("#network-add-slider").val());
        data.append('epochCount', $('#learning-speed-add').val())
        deferred = $.ajax({
            type: 'POST',
            processData: false,
            contentType: false,
            url: 'api/learnDigit',
            data: data
        });
        deferred.done(function(response) {
            if (!response.ok) {
                console.log(response.error);
            } else {
                console.log('success');
            }
        });
        deferred.fail(function() {
            console.log('Не удается распознать! Сервер недоступен');
        });
    });
    $('#network-add-modal').modal('hide');
});

$('#teach').click(function() {
    $.ajax({
        type: 'GET',
        url: 'api/learnMnist',
        data: {
            epochCount: $('#learning-speed').val()
                // epochCount: 5
        },
        success: function(response) {
            console.log(response);
        }
    })
});

$('#reset').click(function() {
    $.ajax({
        type: 'GET',
        url: 'api/resetTrain',
        success: function(response) {
            console.log(response);
        }
    })
});