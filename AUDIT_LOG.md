# Bio-Mapping Engine Audit Log

## [2026-07-09] - Task 1: Autor Normalization (COMPLETED)
- **Issue**: Unspecified Authors count regressed from 45.10% to 56.50%.
- **Root Cause**: The `re.split` call in `src/parser/mapper.py` lacked the `re.IGNORECASE` flag, preventing the engine from recognizing author names in uppercase (e.g., "LISA BOURBEAU").
- **Action**: Added `flags=re.IGNORECASE` to `re.split` in `src/parser/mapper.py`.
- **Verification**: 
    - `Unspecified Authors` returned to 45.10%.
    - `Lisa Bourbeau` is now correctly normalized in the output.
    - Verified via `verify_authors_final.py`.

## [2026-07-09] - Task 2: Reduce Empty Fields (IN PROGRESS)
- **Goal**: Reduce Empty Fields from 35.23% to <15%.
- **Status**: Investigating root causes (navigation segments and regex limitations).

## [2026-07-09] - Task 2: Noise Filtering (SUB-STEP) (COMPLETED)
- **Issue**: Segments like "DICCIONARIO", "DE", etc., were being treated as symptoms, increasing Empty Fields and noise.
- **Action**: Implemented a BLACKLIST filter in `map_segment` to skip noise segments.
- **Result**: Total items decreased from 980 to 949. Noise removed from `sintoma_canonico`. Empty Fields dropped from 35.23% to 22.35% (even with fewer items).

## [cerrado] Tarea 2: Reducción de Empty Fields
- Causa raíz 1: El header_pattern del fallback global no filtraba encabezados de navegación (índice, títulos de sección) tratados como síntomas -> filtro de blacklist agregado en map_segment().
- Causa raíz 2: El fallback capturaba el nombre del síntoma pegado al inicio del contenido, en vez de solo el texto real -> fix con header_pattern.sub() en la lógica de limpieza de fallback.
