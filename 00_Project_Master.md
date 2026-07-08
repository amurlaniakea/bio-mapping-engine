# 🧬 Bio-Mapping Engine: Proyecto de Consulta de Biodescodificación

> **Estado:** 🔍 Fase de Investigación y Reflexión
> **Licencia:** AGPL-3.0-or-later
> **Objetivo:** Crear un motor de consulta multivectorial basado en la literatura de biodescodificación para mapear síntomas, dolencias y zonas anatómicas.

---

## 🎯 Visión del Proyecto
Desarrollar un repositorio y una herramienta de software que permita al usuario navegar por el conocimiento de la biodescodificación no de forma alfabética, sino **topológica** (por localización física). El usuario debe poder encontrar el "sentido biológico" de un malestar mediante tres ejes de entrada.

## 📚 Fuentes de Datos (Dataset)
*   **Fuente Primaria:** `Biodescodificacion.pdf` (Autor: Joan Marc Vilanova i Pujó).
*   **Metodología de uso:** El PDF servirá como base de datos de referencia (Data Test) para la extracción y estructuración de información.
*   **Fuentes de Referencia (Citas):**
    *   Enric Corbera Institute (Diccionario de Biodescodificación).
    *   Escuela de Descodificación Biológica (Christian Flèche).

## 🛠️ Arquitectura de Consulta (Los 3 Vectores)
El motor de búsqueda debe procesar la intersección de:
1.  **Vector de Dolencia:** (Ej: Gastritis, Psoriasis).
2.  **Vector de Localización:** (Ej: Estómago, Piel, Columna).
3.  **Vector de Síntoma:** (Ej: Ardor, Picor, Rigidez).

## ⚖️ Marco Ético y Legal (Compliance)
*   **Licencia:** AGPL-3.0.
*   **Disclaimer Obligatorio:** El software es una herramienta de consulta de literatura alternativa. **NO** sustituye el diagnóstico médico profesional. El usuario es responsable de su propia salud.
*   **Integridad de la Fuente:** Se darán créditos explícitos a los autores originales en el README y en los outputs de la herramienta.

## 🗺️ Mapa de Conceptos (Ontología en desarrollo)
*   [ ] **Mapeo Anatómico:** Relacionar términos coloquiales con términos del PDF (Ej: "Panza" $\rightarrow$ "Abdomen/Estómago").
*   [ ] **Jerarquía de Zonas:** Definir niveles (Sistema $\rightarrow$ Órgano $\rightarrow$ Parte específica).
*   [ ] **Relación de Conflictos:** Vincular el síntoma con la descripción emocional del texto original.

---

## 🚀 Método SDD (Spec-Driven Development) aplicado al Proyecto

Para este proyecto, utilizaremos el ciclo **SDD nivel Spec-anchored** para garantizar que el código sea un reflejo exacto de la investigación previa.

### Fase 1: Constitución (Estructura de Proyecto)
*   Definición de la misión y valores.
*   Establecimiento del tech-stack.
*   Creación de la estructura de carpetas profesional.

### Fase 2: Specification (La "Ancla" de Verdad)
*   Redacción de la `spec.md`.
*   **Criterios de Aceptación (Must-have):**
    1. El programa debe devolver el texto literal del PDF.
    2. La búsqueda debe permitir el uso de al menos 2 de los 3 vectores simultáneamente.
    3. El output debe incluir la referencia de la fuente.
    4. El programa debe manejar términos sinónimos básicos.

### Fase 3: Planning (El Mapa de Tareas)
*   Descomposición de la `spec.md` en un `plan.md` con commits atómicos.
*   Creación de la lista de tareas `tasks.md`.

### Fase 4: Implementation (Ejecución por Micro-pasos)
*   Desarrollo de scripts de extracción (Scraping/Parsing del PDF).
*   Construcción del motor de búsqueda (Mapping Engine).
*   Interfaz de usuario (CLI).

### Fase 5: Verification (El Filtro de Calidad)
*   **Test de Verdad:** Comparar el resultado del programa con una búsqueda manual en el PDF original.
*   **Auditoría de Disclaimer:** Verificar que todas las salidas y el README cumplan con la nota de advertencia médica.

---

## 📝 Notas de Reflexión y Pendientes
*   *Pendiente:* Decidir si la arquitectura será Bottom-Up o Top-Down.
*   *Pendiente:* Definir la estrategia de normalización de términos (Sinónimos).
