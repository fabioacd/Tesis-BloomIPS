var ArchivosPaciente = function () {
    var tabla;
    var all_archivos; //Array donde se almacenan todos los archivos enviados desde el back
    var archivo_paciente = []; //Array donde se almacenarán los archivos del paciente con id: id_paciente


    var init_datatable = function () {
        tabla = $("#tabla_archivos_paciente").DataTable(
            {

                "language": {
                    "url": "//cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
                },
                "scrollX": true

            }
        );
    };
    var onchange_paciente = function () {
        $("#id_paciente").change(function () {
            var id_paciente = this.value;
            if (id_paciente !== '') {
                obtener_archivos_paciente();
                mostrar_archivos_paciente();
            }
            else {
                $("#id_descripcion").val('');
                this.form.reset();
                archivo_paciente = [];
                //Se muestra mensaje en tabla
                mostrar_archivos_paciente();
            }
        });
    };

    var obtener_archivos_paciente = function () {
        archivo_paciente = [];
        var id_paciente = $("#id_paciente").val();
        $.each(all_archivos, function (index, item) {
            if (item.fields.paciente == id_paciente) {
                archivo_paciente.push({
                    'descripcion': item.fields.descripcion,
                    'archivo': item.fields.archivo,
                    'id': item.pk
                });
            }
        });
    };

    var mostrar_archivos_paciente = function () {
        tabla.clear().draw();
        var filas = [];
        if (Array.isArray(archivo_paciente) && archivo_paciente.length) {
            $.each(archivo_paciente, function (index, item) {
                filas = [];
                filas.push("<div style='width: 100%' class='text-justify'>" +
                    "<span>" + item.descripcion + "</span>" +
                    "</div>");

                filas.push("<div style='display: inline-block; white-space: nowrap; width: 100%' class='centrado'>" +
                    "<a style='display: inline;' class='btn-sm btn-block btn-primary centrado' target='_blank' href='/media/" + item.archivo+ "'> Ver </a>" +
                    "<span></span>" +
                    "<a style='display: inline; margin-left: 5px' href='javascript:;' onclick='ArchivosPaciente.openModal("+item.id+")' " +
                    "class='btn-sm btn-block btn-danger centrado'> Eliminar </a>" +
                    "</div>");
                tabla.row.add(filas).draw();
            });

        }
        else {
            filas.push("<div style='width: 100%' class='centrado'>" +
                "<span> Seleccione un paciente para visualizar sus archivos correspondientes </span>" +
                "</div>");
            filas.push("")
        }
    };

    var eliminar_archivo_paciente = function (id_archivo) {
        $.ajax({
            url: "/paciente/eliminar_archivo_paciente_ajax",
            data: {'id_archivo': id_archivo},
            dataType: 'json',
            success: function (data) {
                mensaje_toastr('error', 'Archivo eliminado correctamente.');

                $.each(all_archivos, function (index, item) {
                    if(item.pk == id_archivo){
                        all_archivos.splice(index, 1); //Se elimina de 'Todos los archivos'
                        return false;
                    }
                });
                $('#modal-default').modal('hide');
                // Se vuelve a mostrar los archivos del paciente
                obtener_archivos_paciente();
                mostrar_archivos_paciente();

            }
        });

    };

    return {
        init: function (archivos) {
            init_datatable();
            onchange_paciente();
            all_archivos = archivos;
        },
        openModal: function(idArchivo){
            $('#modal-default').modal('show');
            $('#info_mostrar').html('Está seguro que desea eliminar el archivo?')
            $('#btn_eliminar_archivo').click(function () {
                ArchivosPaciente.eliminar_archivo_paciente(idArchivo);
            });
        },
        eliminar_archivo_paciente: function (id_archivo) {
            eliminar_archivo_paciente(id_archivo)
        }
    };
}();