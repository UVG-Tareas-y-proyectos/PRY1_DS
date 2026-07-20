# Fuentes y catálogos

## Fuente educativa

MINEDUC, Búsqueda de centros educativos autorizados: https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/.

Se ejecutan 23 consultas territoriales, incluyendo Ciudad Capital separada de Guatemala, con nivel DIVERSIFICADO (46) y otros filtros TODOS. Se incluyen todos los estados administrativos. Cada fila es un código de servicio y no necesariamente un establecimiento físico único.

La página sirve una tabla HTML en UTF-8. El programa valida las 17 columnas y el total anunciado por el portal; omite únicamente la columna visual de selección y el pie decorativo vacío. Los valores se transcriben a CSV sin recortar espacios o reemplazar marcadores. La celda HTML NBSP usada para ausencia se serializa vacía.

## Referencia territorial externa

Instituto Nacional de Bosques, capa pública de monitoreo: https://sig.inab.gob.gt/server/rest/services/Hosted/service_fff38eb7eac44746a91435fc53d2b5d1/FeatureServer/7?f=pjson.

Se usa el dominio `codmuni_i`, con 340 códigos y nombres municipales. Los dos primeros dígitos identifican el departamento. `data/catalogos/municipios.csv` conserva la copia utilizada; `fuente.json` registra procedencia y fecha. No se construye el catálogo municipal a partir de los mismos nombres que se pretenden validar.

## Equivalencias controladas

Se permiten únicamente correspondencias explícitas del código territorial entre las variantes del MINEDUC y el dominio externo: Alotenango, San José, Génova Costa Cuca, San Miguel Panam, Santo Tomás Chichicastenango, San Miguel Uspantán, Pachalun y La Tinta. Véase `equivalencias_municipios.json`. La comparación ignora acentos y espacios para localizar la forma canónica; el resultado conserva la grafía del catálogo. No se aplica una corrección geográfica por similitud difusa.

Los códigos de Ciudad Capital comienzan por 00 y el siguiente segmento representa zona, no código municipal INE. Se comprueba la coincidencia de zona, se guarda `ZONA_CAPITAL` y se asigna el municipio Guatemala 0101. El código educativo original se conserva completo.

## Categorías y distritos

`categorias.json` enumera los dominios administrativos del MINEDUC observados y admitidos por el proyecto. No es un catálogo independiente de municipios. Incluye los estados cerrados y temporales, los planes semipresenciales, SIN JORNADA y SIN ESPECIFICAR. El perfil registra todas las frecuencias antes y después. Una nueva categoría produce un fallo de validación en vez de integrarse silenciosamente.

La variable DEPARTAMENTAL representa una dirección administrativa y puede diferir del departamento territorial: Guatemala se divide en Norte/Sur/Oriente/Occidente; Quiché puede incluir Quiché Norte. Se preserva esa distinción.

No se localizó un catálogo público de distrito que permita completar códigos parciales. Se conservan los dos patrones observados y se marca la ausencia o incompletitud. La fuente original y las alertas quedan disponibles para revisión.
