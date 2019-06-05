var Paciente = function () {

    var onchange_tipo_paciente = function () {
        $("#tipo_paciente").on("click", function () {
            var selected_value = $("#tipo_paciente").val();
            if (selected_value == "Adulto") {
                $(".adult").show();
                $(".infant").hide();
                $("#id_tipo_identificacion").val('Cedula ciudadania').trigger('change.select2');
            } else if (selected_value == "Infante") {
                $(".infant").show();
                $(".adult").hide();
                $("#id_tipo_identificacion").val('Tarjeta de identidad').trigger('change.select2');
            } else {
                $(".adult").hide();
                $(".infant").hide();
                $("#id_tipo_identificacion").val('').trigger('change.select2');
            }
        });
    };

    var buscar_cie10 = function () {
        var codigo_palabra = $("#codigo_palabra_cie10").val()
        $.ajax({
            url: "/paciente/get_diagnosticos_ajax",
            data: {'codigo_palabra': codigo_palabra},
            dataType: 'json',
            success: function (data) {
                $("#codigo_palabra_cie10").val('');
                var diagnosticos = JSON.parse(data);
                eliminar_opciones_no_seleccionadas_cie10();
                $.each(diagnosticos, function (index, item) {
                    agregar_opciones_cie10_select(item);
                });
            }
        });
    };

    var eliminar_opciones_no_seleccionadas_cie10 = function () {
        if ($('#id_diagnosticos_cie10 option:selected').length == 0) {
            $("#id_diagnosticos_cie10").empty().trigger('change.select2')
        }
        else {
            $("#id_diagnosticos_cie10").find("option").each(function (index, opt) {
                var flag = false;
                $("#id_diagnosticos_cie10").find("option:selected").each(function (i, selected) {
                    if (opt === selected) {
                        flag = true;
                        return false;
                    }
                });
                if (!flag) {
                    $("#id_diagnosticos_cie10").find('option[value=' + opt.value + ']').remove().trigger('change.select2')
                }
            });
        }
    };

    var agregar_opciones_cie10_select = function (item) {
        var flag = false;
        $("#id_diagnosticos_cie10").find("option").each(function (index, opt) {
            if (opt.value === item.id) {
                flag = true;
                return false;
            }
        });
        if (!flag) {
            var newOption = "<option value='"+item.id+"'> "+item.descripcion+" </option>"
            // var newOption = new Option(item.descripcion, item.id, false, false);
            $("#id_diagnosticos_cie10").append(newOption).trigger('change.select2');
        }
    };

    return {
        init: function () {
            onchange_tipo_paciente();
        },
        buscar_cie10: function () {
            buscar_cie10();
        },
    };

}();
