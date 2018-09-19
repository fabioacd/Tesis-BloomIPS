
$(document).ready(function() {
    $(".numeric").keydown(function(event) {
        //Allow: backspace, delete, tab, escape, and enter

        var reg = /[0-9]\b$/;
        texto = event.key;
        if(texto == 'Tab' || texto =='Backspace'){
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

