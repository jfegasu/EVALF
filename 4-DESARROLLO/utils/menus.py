from flask import session

menuadm = [
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
                {
            "titulo": "SALIR",
            "items": [
                {"texto": "FINALIZAR", "url": "/saliendo","svg":"","fa":"fa fa-power-off"},
                
            ]
        },

    ]

menuapr = [
        {
            "titulo": "INICIO",
            "items": [
                {"texto": "DATOS PERSONALES", "url": "/construir","svg":"","fa":"fa fa-cog"},
                {"texto": "REALIZAR ENCUESTA", "url": "/encuesta","svg":"","fa":"fa fa-book"}
            ]
        },
        {
            "titulo": "SALIR",
            "items": [
                {"texto": "FINALIZAR", "url": "/saliendo","svg":"","fa":"fa fa-power-off"},
                
            ]
        },
]

menuinst = [
        {
            "titulo": "INICIO",
            "items": [
                {"texto": "DATOS PERSONALES", "url": "/construir","svg":"","fa":"fa fa-address-book"},
                {"texto": "CAMBIAR FOTO", "url": "/foto","svg":"","fa":"fa fa-address-book"},
                {"texto": "LISTA DE ASISTENCIA", "url": "/construir","svg":"","fa":"fa fa-address-book"},
                {"texto": "CIERRE DE TRIMESTRE", "url": "/construir","svg":"","fa":"fa fa-address-book"},
                {"texto": "PORTAFOLIO INSTRUCTOR", "url": "/construir","svg":"","fa":"fa fa-address-book"},
 
            ]
        },
        {
            "titulo": "SALIR",
            "items": [
                {"texto": "FINALIZAR", "url": "/saliendo","svg":"","fa":"fa fa-power-off"},
                
            ]
        },
]
def miMenu(tipous):
    if tipous==3:
        menu=menuadm       
    elif tipous==1:
        menu=menuapr
    elif tipous==2:
        menu=menuinst
    return menu

general=[
    {"Titulo":"CRM DE PERSECCION DE LA FORMACION DEL SENA V2.0.0"},
]
def generalApp():
    return general

