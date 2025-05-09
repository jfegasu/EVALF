from models import *
# Configuración de base de datos
db = SqliteDatabase('sena.db')
# ADMIN
Admin.create(NOM='ADMIN', EMAIL='admin@sena.edu.co', CLA='5218f316b3f85b751c613a06aa18010d')

# FICHAINSTRUCTOR
instructores = [
    ('JOSE FERNANDO GALINDO SUAREZ','19407970','3147246','jgalindos@sena.edu.co'),
    ('ULDARICO ANDRADE HERNANDEZ','19123456','3147246','uandrade@sena.edu.co'),
    ('ELIZABETH DOMINGUEZ SUEZCUN','2345678','3147246','edominguez@sena.edu.co')
]
for i in instructores:
    FichaInstructor.create(NOMINST=i[0], DNI=i[1], FICHA=i[2], EMAIL=i[3])

# FICHAPRENDIZ
aprendices = [
    ('3147246','1013106019','DUQUE URIBE JUANA VALENTINA','1','5218f316b3f85b751c613a06aa18010d','juanav_duque@soy.sena.edu.co','ANALISIS Y DESARROLLO DE SOFTWARE'),
    ('3147246','1021673398','GUZMAN MARTINEZ ANA MARIA','1','384babc3e7faa44cf1ca671b74499c3b','anam_guzmanm@soy.sena.edu.co','ANALISIS Y DESARROLLO DE SOFTWARE'),
    ('3147246','1023869341','BAYONA RODRIGUEZ NICOLAS SANTIAGO','1','8f187f643090a53e52550571a8e92ad8','SINCORREO','ANALISIS Y DESARROLLO DE SOFTWARE'),
    # ... Agrega el resto aquí siguiendo el mismo formato ...
]
for a in aprendices:
    FichaAprendiz.create(FICHA=a[0], DNIA=a[1], NOMBREAP=a[2], ESTADOAP=a[3], PWDAP=a[4], EMAIL=a[5], TITULACION=a[6])

# MENU
Menu.create(idMenu=3, LUGAR=1, NOM='USUARIOS', RUTA='/', ROL='ADM', ICONO=None)
Menu.create(idMenu=4, LUGAR=1, NOM='INICIO', RUTA='/login', ROL='APR', ICONO='fa fa-bars')

# PREGUNTAS
preguntas = [
    ('El instructor acompaña y orienta la solución de sus dificultades académicas y personales.',1,'NUNCA, DE VEZ EN CUANDO, SIEMPRE'),
    ('El instructor aplica estrategias participativas de trabajo en equipo que le permiten estar activo permanentemente en su proceso de aprendizaje.',1,'NUNCA, DE VEZ EN CUANDO, SIEMPRE'),
    ('El instructor demuestra dominio técnico.',1,'NO, SI'),
    ('El instructor desarrolla la totalidad de los resultados de aprendizaje programados.',1,'NO, SI'),
    ('El instructor es puntual al iniciar las sesiones.',1,'NUNCA, A VECES, SIEMPRE'),
    ('El instructor establece relaciones interpersonales cordiales, armoniosas y respetuosas.',1,'NUNCA, A VECES, SIEMPRE'),
    ('El instructor incentiva al aprendiz a utilizar la plataforma Territorium en el desarrollo de las actividades de aprendizaje.',1,'NUNCA, DE VEZ EN CUANDO, SIEMPRE'),
    ('El instructor le da a conocer el proyecto formativo, la planeación pedagógica y las guiás de aprendizaje.',1,'NUNCA, A VECES, SIEMPRE'),
    ('El instructor le orienta su formación mediante un proyecto formativo.',1,'NUNCA, A VECES, SIEMPRE'),
    ('El instructor le propone fuentes de consulta (Bibliografía,  Webgrafia...) y ayudas que facilitan su proceso de aprendizaje.',1,'NUNCA, A VECES, SIEMPRE'),
    ('El instructor revisa y asesora los planes de mejoramiento.',1,'NUNCA, A VECES, SIEMPRE'),
    ('El instructor se preocupa por su mejoramiento continuo a nivel personal, social y laboral.',1,'NUNCA, A VECES, SIEMPRE')
]
for p in preguntas:
    Pregunta.create(DESCRIPCION=p[0], ESTADO=p[1], VALORES=p[2])
