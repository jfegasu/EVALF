from flask import session
if session['Tipo']==3:
    menu = [
        {
            "titulo": "CONFIGURACION",
            "items": [
                {"texto": "DATOS INICIALES", "url": "/construir","svg":"","fa":"fa fa-address-book"},
                {"texto": "APERTURA ENCUESTA", "url": "/construir","svg":"9211","fa":""}
            ]
        },
        {
            "titulo": "CARGUE DE DATOS",
            "items": [
                {"texto": "CARGA MASIVA", "url": "/CargaInicial","svg":"9981","fa":""},
                {"texto": "APRENDICES", "url": "/construir","svg":"","fa":"fa fa-users"},
                {"texto": "INSTRUCTORES", "url": "/construir","svg":"","fa":"fa fa-graduation-cap"},
                {"texto": "PREGUNTAS", "url": "/construir","svg":"","fa":"fa fa-question"},
            ]
        },
        {
        "titulo": "RESULTADOS",
            "items": [
                {"texto": "EXPORTAR RESULTADOS(CSV)", "url": "/resp","svg":"","fa":"fa fa-table"},
            ]
        },
            {
        "titulo": "AUDITORIA",
            "items": [
                {"texto": "DESCARGA LOG TRANSACCIONES", "url": "/descargarlog","svg":"","fa":"fa fa-cloud-download"},
                {"texto": "VER LOG DE TRANSACCIONES", "url": "/verlog","svg":"","fa":"fa fa-television"},
            ]
        },
    ]
elif 