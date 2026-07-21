# Plan de limpieza

Este plan recoge los problemas del diagnóstico inicial y los controles que deben ejecutarse antes de transformar los datos de origen.

## CODIGO

Problema: Identificador textual; verificar patrón y unicidad.

Regla y justificación: Conservar ceros iniciales y guiones; normalizar solo espacios externos. No inventar ni renumerar códigos.

Riesgo: Perder ceros o confundir códigos de servicio con planteles.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## DISTRITO

Problema: Vacíos, dos longitudes válidas y códigos incompletos 00-.

Regla y justificación: Mantener ambos formatos; retirar espacios externos, convertir marcadores e incompletos en vacío y conservar DISTRITO_ORIGINAL y ESTADO_DISTRITO.

Riesgo: Completar códigos sin evidencia o mezclar sistemas administrativos diferentes.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## DEPARTAMENTO

Problema: 23 consultas territoriales incluyendo Ciudad Capital; escritura sin tildes.

Regla y justificación: Normalizar acentos/espacios por catálogo. CIUDAD CAPITAL se integra en GUATEMALA, con origen y zona conservados.

Riesgo: Confundir Ciudad Capital con un departamento adicional.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## MUNICIPIO

Problema: 354 valores observados en los datos crudos, zonas de capital y variantes ortográficas.

Regla y justificación: Validar código, nombre y departamento con INAB; aceptar solo equivalencias explícitas. No aplicar unificación difusa.

Riesgo: Confundir zonas con municipios; nombres homónimos entre departamentos.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## ESTABLECIMIENTO

Problema: Espacios múltiples y variantes; posibles coincidencias parciales.

Regla y justificación: Unicode NFC, espacios uniformes y mayúsculas. Mantener tildes existentes, siglas y puntuación con significado; no fusionar nombres automáticamente.

Riesgo: Fusionar centros distintos por semejanza de nombres.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## DIRECCION

Problema: Vacíos, puntos de ausencia, abreviaturas y espacios múltiples.

Regla y justificación: Convertir marcadores explícitos en vacío; retirar caracteres invisibles y espacios repetidos; expandir AV./AVDA./AVEN. y uniformar KM. sin modificar números.

Riesgo: Modificar números de casa, guiones o referencias necesarias.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## TELEFONO

Problema: Vacíos, números múltiples, letras, notas, separadores y longitudes inválidas.

Regla y justificación: Unir grupos 4+4 y retirar prefijo explícito +502/(502); separar números completos sin completar rangos, teléfonos antiguos o dígitos faltantes. Mantener original, estado y notas.

Riesgo: Inventar dígitos, confundir rangos/extensiones con números completos.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## SUPERVISOR

Problema: Marcadores de ausencia y diferencias de espacios/escritura.

Regla y justificación: Normalizar Unicode, espacios y mayúsculas; marcadores de ausencia a vacío; conservar tildes, partículas y apellidos compuestos.

Riesgo: Alterar tildes, partículas o apellidos compuestos; imputar personas inexistentes.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## DIRECTOR

Problema: Vacíos, SIN DATO, guiones, punto, S/D y espacios múltiples.

Regla y justificación: Mismo tratamiento que SUPERVISOR. Se conserva el valor original para revisar marcadores y escritura.

Riesgo: Tratar marcadores como nombres o inferir identidades no verificadas.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## NIVEL

Problema: Comprobar valor constante DIVERSIFICADO.

Regla y justificación: Normalizar texto y comprobar que todas las filas correspondan al nivel 46.

Riesgo: Mezclar otros niveles educativos.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## SECTOR

Problema: Verificar dominio y consistencia de escritura.

Regla y justificación: Uniformar escritura contra catálogo; conservar oficial, privado, municipal y cooperativa como categorías distintas.

Riesgo: Fusionar sectores administrativamente diferentes.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## AREA

Problema: Verificar dominio y categorías informativas.

Regla y justificación: Uniformar escritura. SIN ESPECIFICAR permanece como categoría informada y no se reemplaza por ausencia.

Riesgo: Convertir SIN ESPECIFICAR en una localización inventada.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## STATUS

Problema: Validar dominio con todos los estados administrativos.

Regla y justificación: Conservar cierres temporales, definitivos y estados temporales. No filtrar a establecimientos abiertos.

Riesgo: Excluir cierres o mezclar estados temporales y definitivos.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## MODALIDAD

Problema: Comprobar categorías permitidas.

Regla y justificación: Normalizar texto contra catálogo sin inferir idioma específico.

Riesgo: Inferir idiomas no registrados.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## JORNADA

Problema: Verificar dominio y preservar diferencias operativas.

Regla y justificación: Uniformar escritura; SIN JORNADA se conserva separada de la ausencia. No fusionar jornadas.

Riesgo: Fusionar jornadas o convertir SIN JORNADA en ausencia.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## PLAN

Problema: Variantes de formato; validar sin fusionar frecuencias distintas.

Regla y justificación: Mantener planes diarios, de fin de semana, virtuales y semipresenciales diferenciados. Normalización por equivalencia de acentos/caso/espacios.

Riesgo: Unificar planes de atención con significado diferente.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## DEPARTAMENTAL

Problema: Regiones administrativas no equivalentes a departamentos.

Regla y justificación: Normalizar por catálogo; validar correspondencia con departamento territorial, sin confundir región administrativa con departamento.

Riesgo: Confundir región administrativa con departamento territorial.

Control: Conservar crudo, original cuando aplica y registrar cada celda modificada.

## Duplicados y validación

Separar duplicados exactos, códigos repetidos y semejanza parcial. Comparar dentro de municipio y conservar todo servicio sin evidencia de error. Registrar los pares, decisiones y justificaciones. Ejecutar contratos de formato, tipo, dominio y coherencia territorial antes de publicar el conjunto limpio.
