var ConsultarEvoDiaria = function () {
    var id_empleado;
    var cargo_empleado;

    var init_form = function () {
        var d = new Date();
        var mes = d.getMonth()+1;
        var dia = d.getDate();
        var output =  (mes<10 ? '0' : '') + mes + '/' + (dia<10 ? '0' : '') + dia + '/' + d.getFullYear();

        //Date range picker
        $('#rango_fecha').daterangepicker({
            autoclose: true,
            language: "es",
            maxDate: output,
            "locale": {
              format: 'MM/DD/YYYY',
              separator: ' - ',
              applyLabel: 'Aplicar',
              cancelLabel: 'Cancelar',
              fromLabel: 'Desde',
              toLabel: 'Hasta',
              customRangeLabel: 'Custom',
              weekLabel: 'W',
              daysOfWeek: ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie','Sab'],
              monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
              firstDay: 1
            }
        });
        //Se agrega opción de 'todas' en select de área
        var component = "<option value='all' name='all_areas'> Todas </option>";
        $("#id_area").append(component);
    };

    var onclick_hist_clinica = function () {
        var id_paciente_select = $('#id_paciente').val();

            if(id_paciente_select){
                $('#form-consolidado').submit();
            }
            else{
                mensaje_toastr('warning', 'Por favor seleccione un paciente.');
            }
    };

    var onchange_area_fecha = function () {
        $('#id_area, #rango_fecha').change(function () {
            var area = $('#id_area').val();
            var fechas = $('#rango_fecha').val();
            $('#id_paciente').empty();
            if (area == '') {
                $('.div-generar-pdf').addClass('hidden');
            } else {
                $.ajax({
                    url: "/paciente/get_pacientes_ent_ajax",
                    data: {'area': area, 'id_empleado': id_empleado, 'rango_fecha': fechas},
                    method: 'GET',
                    dataType: 'json',
                    success: function (data) {
                        var paciente_comp = "<option value=''> Seleccione paciente </option>";
                        $("#id_paciente").append(paciente_comp);
                        var json = JSON.parse(data)
                        var json_size = Object.keys(json).length;
                        for (var i = 0; i < json_size; i++) {
                            id = json[i].id;
                            nombre = json[i].nombre;
                            apellido = json[i].apellido;
                            identificacion = json[i].identificacion;
                            $("#id_paciente").append('<option value="' + id + '">' + identificacion + " - " + nombre + " " + apellido + '</option>');
                        }
                    }
                });
            }
        });
    };

    var onchange_paciente = function () {
        $('#id_paciente').change(function () {
            var id_paciente = $('#id_paciente').val();

            if(id_paciente && (cargo_empleado != 'Terapeuta')){
                $('.div-generar-pdf').removeClass('hidden');
            }
            else{
                $('.div-generar-pdf').addClass('hidden');
            }
        });
    };

    return {
        init: function (empleado_actual, cargo_emp) {
            id_empleado = empleado_actual;
            cargo_empleado = cargo_emp;
            init_form();
            onchange_area_fecha();
            onchange_paciente();
        },
        onclick_hist_clinica: function () {
            onclick_hist_clinica();
        }
    };

}();
