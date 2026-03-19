# 🧾 Data Dictionary

Este documento describe las variables utilizadas en el proyecto. Úsalo como referencia para comprender el significado, tipo y posibles valores de cada campo.

## Tabla: [NOMBRE_DE_LA_TABLA]

| Variable         | Tipo de Dato | Descripción                                | Valores Posibles / Rango                   |
|------------------|--------------|--------------------------------------------|--------------------------------------------|
| id_cliente       | Entero       | Identificador único del cliente            | Numérico único                              |
| edad             | Entero       | Edad del cliente                           | 18 - 99                                     |
| genero           | Categórica   | Género del cliente                         | 'M', 'F', 'Otro'                            |
| ingreso_mensual  | Float        | Ingreso mensual estimado del cliente       | En moneda local                             |
| fecha_registro   | Fecha        | Fecha en la que el cliente se registró     | YYYY-MM-DD                                  |
| ...              | ...          | ...                                        | ...                                         |

### Notas:

- Las variables categóricas deben tener codificación clara si se transforman.
- Los campos derivados deben marcarse como tal.
- Incluir cualquier transformación o imputación realizada.

### Ejemplos:

- `genero`: Esta variable fue codificada a números durante el entrenamiento del modelo (`M=0`, `F=1`, `Otro=2`, `No especificado=3`).
- `score_crediticio`: Variable derivada. Se calcula con un modelo propietario y **no está presente en los datos originales**.
- Los valores faltantes en `ingreso_mensual` fueron imputados con la mediana por segmento de edad.
