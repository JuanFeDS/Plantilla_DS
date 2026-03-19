# RFC-XXX: [Título del RFC]

**Estado**: [Draft / En Revisión / Aprobado / Rechazado / Implementado]  
**Autor**: [Nombre del autor]  
**Fecha de creación**: YYYY-MM-DD  
**Última actualización**: YYYY-MM-DD  
**Revisores**: [@persona1, @persona2]  
**Stakeholders**: [Lista de stakeholders afectados]

---

## 📋 Resumen

[Breve descripción de 2-3 párrafos del cambio propuesto, su motivación y el impacto esperado]

---

## 🎯 Motivación

### Problema Actual

[Descripción detallada del problema que se está resolviendo o la oportunidad que se está aprovechando]

**Síntomas**:
- Síntoma 1
- Síntoma 2
- Síntoma 3

**Impacto del problema**:
- Impacto en negocio
- Impacto técnico
- Impacto en usuarios

### Objetivos

**Objetivos principales**:
1. Objetivo 1
2. Objetivo 2
3. Objetivo 3

**Objetivos secundarios**:
- Objetivo secundario 1
- Objetivo secundario 2

**No objetivos** (fuera de scope):
- No objetivo 1
- No objetivo 2

---

## 💡 Propuesta

### Descripción de la Solución

[Descripción detallada de la solución propuesta]

#### Componentes Principales

1. **Componente 1**
   - Descripción
   - Responsabilidad
   - Interacciones

2. **Componente 2**
   - Descripción
   - Responsabilidad
   - Interacciones

### Arquitectura Propuesta

```
[Diagrama de arquitectura en ASCII o link a diagrama]

┌─────────────┐
│  Component  │
│      A      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Component  │
│      B      │
└─────────────┘
```

### Cambios Específicos

#### Código

**Archivos nuevos**:
- `path/to/new_file.py`: [Descripción]
- `path/to/another_file.py`: [Descripción]

**Archivos modificados**:
- `path/to/existing_file.py`: [Qué cambia]
- `path/to/another_existing.py`: [Qué cambia]

**Archivos eliminados**:
- `path/to/deprecated_file.py`: [Por qué se elimina]

#### Datos

**Nuevas tablas/colecciones**:
- `tabla_nueva`: [Schema y propósito]

**Modificaciones a schema**:
- `tabla_existente`: [Qué columnas se agregan/modifican/eliminan]

**Migraciones necesarias**:
- Migración 1: [Descripción]
- Migración 2: [Descripción]

#### Infraestructura

**Nuevos recursos**:
- Recurso 1: [Descripción y especificaciones]
- Recurso 2: [Descripción y especificaciones]

**Modificaciones**:
- Recurso existente: [Qué cambia]

#### Configuración

**Variables de entorno nuevas**:
```bash
NEW_VAR_1=value  # Descripción
NEW_VAR_2=value  # Descripción
```

**Configuraciones modificadas**:
- Config 1: [Cambio]
- Config 2: [Cambio]

---

## 🔄 Alternativas Consideradas

### Alternativa 1: [Nombre]

**Descripción**: [Breve descripción]

**Pros**:
- Pro 1
- Pro 2

**Contras**:
- Contra 1
- Contra 2

**Razón de rechazo**: [Por qué no se eligió esta alternativa]

### Alternativa 2: [Nombre]

**Descripción**: [Breve descripción]

**Pros**:
- Pro 1
- Pro 2

**Contras**:
- Contra 1
- Contra 2

**Razón de rechazo**: [Por qué no se eligió esta alternativa]

### No hacer nada (Status Quo)

**Consecuencias de no implementar**:
- Consecuencia 1
- Consecuencia 2

---

## 📊 Análisis de Impacto

### Impacto en Performance

| Métrica | Actual | Propuesto | Cambio |
|---------|--------|-----------|--------|
| Latencia (p95) | XXms | XXms | ±XX% |
| Throughput | XX req/s | XX req/s | ±XX% |
| Uso de CPU | XX% | XX% | ±XX% |
| Uso de Memoria | XX GB | XX GB | ±XX GB |

**Análisis**: [Explicación del impacto]

### Impacto en Modelo

| Métrica | Baseline | Propuesto | Cambio |
|---------|----------|-----------|--------|
| Accuracy | 0.XX | 0.XX | ±X% |
| Precision | 0.XX | 0.XX | ±X% |
| Recall | 0.XX | 0.XX | ±X% |
| F1 Score | 0.XX | 0.XX | ±X% |

**Análisis**: [Explicación del impacto]

### Impacto en Negocio

**Métricas de negocio afectadas**:
- Métrica 1: [Impacto esperado]
- Métrica 2: [Impacto esperado]

**ROI estimado**:
- Costo de implementación: $X,XXX
- Beneficio anual estimado: $X,XXX
- Payback period: X meses

### Impacto en Usuarios

**Usuarios afectados**: [Número y tipo de usuarios]

**Cambios visibles**:
- Cambio 1
- Cambio 2

**Experiencia de usuario**:
- Mejora 1
- Mejora 2

### Impacto en Equipo

**Esfuerzo de desarrollo**:
- Estimación: X días/persona
- Equipo necesario: [Roles]

**Esfuerzo de mantenimiento**:
- Incremento/Reducción: [Descripción]

**Deuda técnica**:
- Deuda agregada: [Descripción]
- Deuda reducida: [Descripción]

---

## 🔒 Riesgos y Mitigaciones

### Riesgo 1: [Nombre del riesgo]

**Probabilidad**: [Alta / Media / Baja]  
**Impacto**: [Alto / Medio / Bajo]  
**Severidad**: [Crítico / Alto / Medio / Bajo]

**Descripción**: [Descripción detallada del riesgo]

**Mitigación**:
- Acción 1
- Acción 2

**Plan de contingencia**:
- Si ocurre, hacer X
- Rollback plan: [Descripción]

### Riesgo 2: [Nombre del riesgo]

**Probabilidad**: [Alta / Media / Baja]  
**Impacto**: [Alto / Medio / Bajo]  
**Severidad**: [Crítico / Alto / Medio / Bajo]

**Descripción**: [Descripción detallada del riesgo]

**Mitigación**:
- Acción 1
- Acción 2

**Plan de contingencia**:
- Si ocurre, hacer X
- Rollback plan: [Descripción]

---

## ✅ Criterios de Éxito

### Métricas de Éxito

**Métricas técnicas**:
- [ ] Métrica 1: [Threshold de éxito]
- [ ] Métrica 2: [Threshold de éxito]

**Métricas de negocio**:
- [ ] Métrica 1: [Threshold de éxito]
- [ ] Métrica 2: [Threshold de éxito]

**Métricas de calidad**:
- [ ] Cobertura de tests > XX%
- [ ] Documentación completa
- [ ] Code review aprobado

### Condiciones de Aceptación

- [ ] Condición 1
- [ ] Condición 2
- [ ] Condición 3

---

## 🗓️ Plan de Implementación

### Fases

#### Fase 1: Preparación (Semana 1)

**Objetivos**:
- Objetivo 1
- Objetivo 2

**Tareas**:
- [ ] Tarea 1 (Responsable: @persona, Estimación: X días)
- [ ] Tarea 2 (Responsable: @persona, Estimación: X días)

**Entregables**:
- Entregable 1
- Entregable 2

#### Fase 2: Desarrollo (Semanas 2-3)

**Objetivos**:
- Objetivo 1
- Objetivo 2

**Tareas**:
- [ ] Tarea 1 (Responsable: @persona, Estimación: X días)
- [ ] Tarea 2 (Responsable: @persona, Estimación: X días)

**Entregables**:
- Entregable 1
- Entregable 2

#### Fase 3: Testing (Semana 4)

**Objetivos**:
- Objetivo 1
- Objetivo 2

**Tareas**:
- [ ] Tarea 1 (Responsable: @persona, Estimación: X días)
- [ ] Tarea 2 (Responsable: @persona, Estimación: X días)

**Entregables**:
- Entregable 1
- Entregable 2

#### Fase 4: Deployment (Semana 5)

**Objetivos**:
- Objetivo 1
- Objetivo 2

**Tareas**:
- [ ] Tarea 1 (Responsable: @persona, Estimación: X días)
- [ ] Tarea 2 (Responsable: @persona, Estimación: X días)

**Entregables**:
- Entregable 1
- Entregable 2

### Timeline

```
Semana 1: Preparación
Semana 2-3: Desarrollo
Semana 4: Testing
Semana 5: Deployment
```

**Hitos clave**:
- YYYY-MM-DD: Hito 1
- YYYY-MM-DD: Hito 2
- YYYY-MM-DD: Go-live

### Dependencias

**Dependencias externas**:
- Dependencia 1: [Descripción, responsable, fecha esperada]
- Dependencia 2: [Descripción, responsable, fecha esperada]

**Dependencias internas**:
- Dependencia 1: [Descripción, responsable]
- Dependencia 2: [Descripción, responsable]

---

## 🧪 Plan de Testing

### Tests Unitarios

**Cobertura objetivo**: XX%

**Áreas críticas a testear**:
- Área 1
- Área 2

### Tests de Integración

**Escenarios**:
- Escenario 1: [Descripción]
- Escenario 2: [Descripción]

### Tests de Performance

**Benchmarks**:
- Benchmark 1: [Descripción y threshold]
- Benchmark 2: [Descripción y threshold]

### Tests de Regresión

**Suite de regresión**:
- Test 1
- Test 2

### A/B Testing (si aplica)

**Diseño del experimento**:
- Grupo control: [Descripción]
- Grupo tratamiento: [Descripción]
- Duración: X días
- Tamaño de muestra: X usuarios

**Métricas a medir**:
- Métrica 1
- Métrica 2

---

## 📚 Documentación

### Documentación a Actualizar

- [ ] README.md
- [ ] API documentation
- [ ] Model card
- [ ] Deployment guide
- [ ] Runbooks

### Documentación Nueva

- [ ] Documento 1: [Descripción]
- [ ] Documento 2: [Descripción]

### Training Necesario

**Audiencia**: [Quién necesita training]

**Contenido**:
- Tema 1
- Tema 2

**Formato**: [Workshop, documentación, video, etc.]

---

## 🔄 Plan de Rollback

### Condiciones de Rollback

Hacer rollback si:
- Condición 1
- Condición 2
- Condición 3

### Procedimiento de Rollback

**Paso 1**: [Descripción]
```bash
# Comandos si aplica
```

**Paso 2**: [Descripción]
```bash
# Comandos si aplica
```

**Tiempo estimado de rollback**: X minutos

### Validación Post-Rollback

- [ ] Verificación 1
- [ ] Verificación 2

---

## 💬 Preguntas Abiertas

1. **Pregunta 1**: [Descripción]
   - Opciones: A, B, C
   - Recomendación: [Opción recomendada y por qué]

2. **Pregunta 2**: [Descripción]
   - Opciones: A, B, C
   - Recomendación: [Opción recomendada y por qué]

---

## 📝 Decisiones

### Decisión 1: [Título]

**Fecha**: YYYY-MM-DD  
**Decidido por**: [@persona]  
**Decisión**: [Descripción]  
**Rationale**: [Justificación]

### Decisión 2: [Título]

**Fecha**: YYYY-MM-DD  
**Decidido por**: [@persona]  
**Decisión**: [Descripción]  
**Rationale**: [Justificación]

---

## 🔗 Referencias

- [Documento relacionado 1](link)
- [Documento relacionado 2](link)
- [RFC relacionado](link)
- [Issue/Ticket](link)

---

## 📋 Historial de Cambios

| Fecha | Versión | Autor | Cambios |
|-------|---------|-------|---------|
| YYYY-MM-DD | 0.1 | [@autor] | Versión inicial |
| YYYY-MM-DD | 0.2 | [@autor] | Incorporar feedback de revisión |
| YYYY-MM-DD | 1.0 | [@autor] | Versión aprobada |

---

## ✍️ Aprobaciones

| Rol | Nombre | Fecha | Estado |
|-----|--------|-------|--------|
| Tech Lead | [@nombre] | YYYY-MM-DD | ✅ Aprobado |
| Product Owner | [@nombre] | YYYY-MM-DD | ⏳ Pendiente |
| ML Lead | [@nombre] | YYYY-MM-DD | ⏳ Pendiente |
| DevOps | [@nombre] | YYYY-MM-DD | ⏳ Pendiente |

---

## 📧 Contacto

**Autor**: [email@empresa.com]  
**Slack**: #canal-del-proyecto  
**Reunión de revisión**: [Link a calendario]
