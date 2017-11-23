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
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

$('#learning-speed').slider({
    step: 0.01,
    precision: 2,
    tooltip: 'always',
    tooltip_position: 'bottom'
});

$('#result').css({
    width: 14 * 40,
    height: 14 * 40
})

var pad = new Sketchpad({
    element: '#pad',
    width: 14 * 40,
    height: 14 * 40
});

setInterval(function () {
    for (var i = 0; i < 10; i++) {
        var value = getRandomInt(0, 100);
        var myclass = "progress-bar progress-bar-striped progress-bar-success active";
        if (66 >= value && value > 33) {
            myclass = "progress-bar progress-bar-striped progress-bar-warning active";
        }
        if (33 >= value) {
            myclass = "progress-bar progress-bar-striped progress-bar-danger active";
        }
        $('#progress-' + i).prop("class", myclass);
        $('#progress-' + i).css('width', value + '%');
        $('#progress-' + i).text(value + '%');
    }
}, 1000);

setInterval(function () {
    for (var i = 0; i < 10; i++) {
        var value = getRandomInt(0, 100);
        var myclass = "progress-bar progress-bar-striped progress-bar-success active";
        if (66 >= value && value > 33) {
            myclass = "progress-bar progress-bar-striped progress-bar-warning active";
        }
        if (33 >= value) {
            myclass = "progress-bar progress-bar-striped progress-bar-danger active";
        }
        $('#progress-error-' + i).prop("class", myclass);
        $('#progress-error-' + i).css('width', value + '%');
        $('#progress-error-' + i).text(value + '%');
    }
}, 1000)

pad.penSize = 40;
pad.color = 'black';

$('#undo').click(function () {
    pad.undo();
});

$('#redo').click(function () {
    pad.redo();
});

$('#recogniseSubmit').click(function () {
    document.getElementById('pad').toBlob(function (e) {
        var data = new FormData();
        data.append('myFile', e, 'image.png');
        $.ajax({
            type: 'POST',
            processData: false,
            contentType: false,
            url: 'api/recognizePhoto',
            data: data,
            success: function (response) {
                console.log('success!')
            }
        })
    })
});

$('#teach').click(function () {
    $.ajax({
        type: 'POST',
        url: 'api/teach',
        data: {
            'speed': $('#learning-speed').val()
        },
        success: function (response) {
            console.log('success!')
        }
    })
});
