# Libro de códigos preliminar

Alcance: esquema y decisiones propuestas; la limpieza final permanece pendiente. Las 17 variables y el diagnóstico inicial provienen del avance entregado. Se reportaron 11,867 registros de 23 CSV, extraídos el 19 de julio de 2026.

Fuente: https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/. Nivel DIVERSIFICADO; otros filtros TODOS. Unidad: código de servicio educativo, no plantel único.

## CODIGO

Descripción: Código único del servicio educativo autorizado. No identifica necesariamente un plantel físico único.

Tipo previsto: Identificador textual.

Dominio y tratamiento a verificar: Dos dígitos de territorio, dos de municipio/zona, cuatro de servicio y sufijo 46: 00-00-0000-46. Único y no vacío. Conservar ceros iniciales y guiones; normalizar solo espacios externos. No inventar ni renumerar códigos.

## DISTRITO

Descripción: Código de distrito o supervisión educativa informado por el MINEDUC.

Tipo previsto: Identificador textual opcional.

Dominio y tratamiento a verificar: 00-000 o 00-00-0000; vacío si falta o está incompleto. Mantener ambos formatos; retirar espacios externos, convertir marcadores e incompletos en vacío y conservar DISTRITO_ORIGINAL y ESTADO_DISTRITO.

## DEPARTAMENTO

Descripción: Departamento territorial del establecimiento según catálogo oficial.

Tipo previsto: Categórica nominal.

Dominio y tratamiento a verificar: 22 departamentos del catálogo municipios.csv. Normalizar acentos/espacios por catálogo. CIUDAD CAPITAL se integra en GUATEMALA, con origen y zona conservados.

## MUNICIPIO

Descripción: Municipio territorial validado por código. Las zonas de capital se almacenan por separado.

Tipo previsto: Categórica nominal.

Dominio y tratamiento a verificar: Nombres oficiales de los 340 municipios; el nombre puede repetirse en varios departamentos, por lo que se usa CODIGO_MUNICIPIO. Validar código, nombre y departamento con INAB; aceptar solo equivalencias explícitas. No aplicar unificación difusa.

## ESTABLECIMIENTO

Descripción: Nombre del centro educativo asociado al código de servicio.

Tipo previsto: Texto nominal opcional.

Dominio y tratamiento a verificar: Texto de longitud variable o vacío; nombres iguales pueden representar servicios o sedes diferentes. Unicode NFC, espacios uniformes y mayúsculas. Mantener tildes existentes, siglas y puntuación con significado; no fusionar nombres automáticamente.

## DIRECCION

Descripción: Dirección física del establecimiento informada en la fuente.

Tipo previsto: Texto opcional.

Dominio y tratamiento a verificar: Texto o vacío; números de casa, guiones y referencias son significativos. Convertir marcadores explícitos en vacío; retirar caracteres invisibles y espacios repetidos; expandir AV./AVDA./AVEN. y uniformar KM. sin modificar números.

## TELEFONO

Descripción: Uno o más teléfonos completos extraídos de la cadena de contacto original.

Tipo previsto: Identificador textual opcional.

Dominio y tratamiento a verificar: Ocho dígitos por número; varios separados por punto y coma; vacío cuando no existe ningún número completo verificable por formato. Unir grupos 4+4 y retirar prefijo explícito +502/(502); separar números completos sin completar rangos, teléfonos antiguos o dígitos faltantes. Mantener original, estado y notas.

## SUPERVISOR

Descripción: Nombre de la persona responsable de supervisión educativa.

Tipo previsto: Texto nominal opcional.

Dominio y tratamiento a verificar: Texto o vacío. No se interpreta como una identidad personal verificada. Normalizar Unicode, espacios y mayúsculas; marcadores de ausencia a vacío; conservar tildes, partículas y apellidos compuestos.

## DIRECTOR

Descripción: Nombre de la persona registrada como directora o director.

Tipo previsto: Texto nominal opcional.

Dominio y tratamiento a verificar: Texto o vacío; no imputar nombres faltantes. Mismo tratamiento que SUPERVISOR. Se conserva el valor original para revisar marcadores y escritura.

## NIVEL

Descripción: Nivel educativo autorizado del servicio.

Tipo previsto: Categórica constante.

Dominio y tratamiento a verificar: DIVERSIFICADO. Normalizar texto y comprobar que todas las filas correspondan al nivel 46.

## SECTOR

Descripción: Tipo de gestión del servicio educativo.

Tipo previsto: Categórica nominal.

Dominio y tratamiento a verificar: Dominio explícito en categorias.json, clave SECTOR. Uniformar escritura contra catálogo; conservar oficial, privado, municipal y cooperativa como categorías distintas.

## AREA

Descripción: Clasificación urbana/rural del establecimiento.

Tipo previsto: Categórica nominal.

Dominio y tratamiento a verificar: URBANA, RURAL o SIN ESPECIFICAR. Uniformar escritura. SIN ESPECIFICAR permanece como categoría informada y no se reemplaza por ausencia.

## STATUS

Descripción: Estado administrativo del código de servicio.

Tipo previsto: Categórica nominal.

Dominio y tratamiento a verificar: Dominio explícito en categorias.json, clave STATUS. Conservar cierres temporales, definitivos y estados temporales. No filtrar a establecimientos abiertos.

## MODALIDAD

Descripción: Modalidad lingüística autorizada del servicio.

Tipo previsto: Categórica nominal.

Dominio y tratamiento a verificar: MONOLINGUE o BILINGUE. Normalizar texto contra catálogo sin inferir idioma específico.

## JORNADA

Descripción: Jornada en la que está autorizado el servicio educativo.

Tipo previsto: Categórica nominal.

Dominio y tratamiento a verificar: Dominio explícito en categorias.json, clave JORNADA. Uniformar escritura; SIN JORNADA se conserva separada de la ausencia. No fusionar jornadas.

## PLAN

Descripción: Plan o frecuencia de atención educativa autorizada.

Tipo previsto: Categórica nominal.

Dominio y tratamiento a verificar: Dominio explícito en categorias.json, clave PLAN. Mantener planes diarios, de fin de semana, virtuales y semipresenciales diferenciados. Normalización por equivalencia de acentos/caso/espacios.

## DEPARTAMENTAL

Descripción: Dirección departamental administrativa responsable del servicio.

Tipo previsto: Categórica nominal.

Dominio y tratamiento a verificar: Regiones autorizadas en categorias.json, clave DEPARTAMENTAL; puede incluir Guatemala Norte/Sur/Oriente/Occidente o Quiché Norte. Normalizar por catálogo; validar correspondencia con departamento territorial, sin confundir región administrativa con departamento.

## Variables derivadas propuestas

El avance propone TELEFONO_LIMPIO y ESTADO_TELEFONO, además de conservar nombres y direcciones originales. La implementación y el libro definitivo se incorporan en la fase final. También será necesario distinguir zona capital de municipio y documentar las comprobaciones de distrito y geografía.

## Metadatos comunes y trazabilidad propuesta

La fuente educativa es el buscador oficial MINEDUC y la unidad de observación es un código de servicio. El manifiesto data/raw/manifest.json contiene los datos de procedencia y las sumas SHA-256 por archivo. El catálogo municipal externo y sus equivalencias se documentan en docs/FUENTES_Y_CATALOGOS.md.

Este libro preliminar es versión 0.1: define campos y reglas previstas, no resultados finales. Las ausencias no se imputarán. Las diferencias de jornada, plan o código impiden asumir que dos servicios son un duplicado por tener un nombre similar. La fase final deberá incluir el registro de transformaciones, las pruebas automáticas y el dominio completo de cada variable derivada.
