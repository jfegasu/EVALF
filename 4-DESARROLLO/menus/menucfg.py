menuap = [
    {
        "titulo": "INICIO",
        "icono": "fas fa-landmark",
        "url": "/login"
    },
    {
        "titulo": "APRENDIZ",
        "icono": "fa fa-child",
        "url": "/maqueta",
        "submenu": [
            {
                "titulo": "PORTAFOLIO DE EVIDENCIAS",
                "icono": "fas fa-paperclip",
                "url": "#"
            },
            {
                "titulo": "DISEÑO",
                "icono": "fas fa-briefcase",
                "url": "#",
                "submenu": [
                    {
                        "titulo": "PROGRAMA DE FORMACION",
                        "icono": "far fa-calendar-alt",
                        "url": "#"
                    },
                    {
                        "titulo": "PROYECTO FORMATIVO",
                        "icono": "fas fa-certificate",
                        "url": "#"
                    },
                    {
                        "titulo": "PLANEACION PEDAGOGICA",
                        "icono": "fas fa-business-time",
                        "url": "#"
                    }
                ]
            },
            {
                "titulo": "ACTIVIDAD DE APRENDIZAJE",
                "icono": "fas fa-edit",
                "url": "#",
                "submenu": [
                    {
                        "titulo": "NOTIFICACIONES",
                        "icono": "fas fa-comments",
                        "url": "#"
                    },
                    {
                        "titulo": "HORARIO",
                        "icono": "fas fa-calendar-alt",
                        "url": "#"
                    },
                    {
                        "titulo": "GUIAS DE APRENDIZAJE",
                        "icono": "fas fa-calendar-alt",
                        "url": "#"
                    }
                ]
            }
        ]
    },
    {
        "titulo": "ENCUESTA",
        "icono": "fa fa-list",
        "url": "/encuesta"
    },
    {
        "titulo": "ACERCA",
        "icono": "fa fa-list",
        "url": "/acerca"
    }
]
menuins = [
    {
        "titulo": "INICIO",
        "icono": "fas fa-landmark",
        "url": "/login"
    },
    {
        "titulo": "INSTRUCTOR",
        "icono": "fa fa-child",
        "url": "/maqueta",
        "submenu": [
            {
                "titulo": "PORTAFOLIO DE EVIDENCIAS",
                "icono": "fas fa-paperclip",
                "url": "#"
            },
            {
                "titulo": "DISEÑO",
                "icono": "fas fa-briefcase",
                "url": "#",
                "submenu": [
                    {
                        "titulo": "PROGRAMA DE FORMACION",
                        "icono": "far fa-calendar-alt",
                        "url": "#"
                    },
                    {
                        "titulo": "PROYECTO FORMATIVO",
                        "icono": "fas fa-certificate",
                        "url": "#"
                    },
                    {
                        "titulo": "PLANEACION PEDAGOGICA",
                        "icono": "fas fa-business-time",
                        "url": "#"
                    }
                ]
            },
            {
                "titulo": "ACTIVIDAD DE APRENDIZAJE",
                "icono": "fas fa-edit",
                "url": "#",
                "submenu": [
                    {
                        "titulo": "NOTIFICACIONES*",
                        "icono": "fas fa-comments",
                        "url": "#"
                    },
                    {
                        "titulo": "HORARIO",
                        "icono": "fas fa-calendar-alt",
                        "url": "#"
                    },
                    {
                        "titulo": "GUIAS DE APRENDIZAJE",
                        "icono": "fas fa-calendar-alt",
                        "url": "#"
                    }
                ]
            }
        ]
    },
    {
        "titulo": "ENCUESTA",
        "icono": "fa fa-list",
        "url": "/encuesta"
    },
    {
        "titulo": "ACERCA",
        "icono": "fa fa-list",
        "url": "/acerca"
    }
]

def getMenu(Cual):
    if Cual == "1":
        return menuap
    if Cual == "2":
        return menuins
    return None
        
