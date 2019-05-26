
$(document).ready(function() {
    $(".numeric").keydown(function(event) {
        //Allow: backspace, delete, tab, escape, and enter

        var reg = /[0-9]\b$/;
        texto = event.key;
        if(texto == 'Tab' || texto =='Backspace' || texto == 'ArrowLeft' || texto == 'ArrowRight' ||
            texto == 'ArrowUp' || texto == 'ArrowDown'){
            return;
        }
        if(reg.test(texto)){
            return;
        }else{
            event.preventDefault();
        }
    });

    $(".alphabetic").keydown(function(event) {
        //Allow: backspace, delete, tab, escape, and enter
        var reg = /[a-zA-Z\ñ\Ñ\á\é\í\ó\ú\s]+$/;
        texto = event.key;
        if(reg.test(texto)){
            return;
        }else{
            event.preventDefault();
        }
    });

    $(".locations").keydown(function(event) {
        //Allow: backspace, delete, tab, escape, and enter
        var reg = /[a-zA-Z\ñ\Ñ\á\é\í\ó\ú\s\,\-]+$/;
        texto = event.key;
        if(reg.test(texto)){
            return;
        }else{
            event.preventDefault();
        }
    });

});

function mensaje_toastr (tag, message) {
    toastr.options = {
        "closeButton": true,
        "progressBar": true,
        "showEasing": "swing",
        "timeOut": 10000
    }
    toastr [tag](message)
};

