# TEG_asovac

Este sistema esta desarrollado en Django y fueron usadas las siguientes herramientas para su desarrollo:

Framework: Django 11.13
Adaptador para conexión con PostgreSQL: psycopg2 2.7.4
Lenguaje servidor: python 2.7.6
Sistema manejador de base de datos: PosgreSQL

## Estructura de los directorios

### Estructura de carpetas

```
├── app/
│   ├── components/
│   ├── performance/
│   │  ├── components/
│   │  ├── reporting/
│   │  │     ├── components/
│   │  │     ├── reporting-routing.config.js
│   │  │     └── reporting.module.js
│   │  ├── performance-routing.config.js
│   │  └── performance.module.js
│   ├── app-routing.config.js
│   └── app.module.js
└── index.html
```

### Forma de escritura

Para la implementacion del codigo se utilizara la convecion de **snake_case** respetando las buenas practicas para el nombre de las funciones,parametros, clases, formularios, variables y constantes

### Configuracion del .env (usando Decouple)

```
API_URL = http://api-local.rankmi.lo:3000/v1
API_REPORTS_URL = http://api-local.rankmi.lo:3002/v1
APP_URL = http://app-local.rankmi.lo:9000/
ASSET_PATH = https://rankmi-prod.s3.amazonaws.com/
AVATAR_PATH = users/avatars/medium/
DEFAULT_AVATAR_PATH = default/icono-persona-01.png
ENV = local
```

### Forma de trabajo utilizando branch

1.-Existira un Branch Master que contendra los cambios ya estables y revisados
2.-Existira un Branch Development donde se se tendran los cambios estables que aun deben ser revisados por 2da vez
3.-Al desarrollar algo nuevo se procede a crear un branch nuevo con el siguiente formato *TEG-XXX* donde ese numero se indicara en la tarea del trello acompañado de una descripcion. Todos los branchs deben salir de development mientras sean funcionaldiades nuevas y si son errores deben salir desde Master. Al ser revisada la tarea por primera vez si esta correcta se hace merge hacia development
