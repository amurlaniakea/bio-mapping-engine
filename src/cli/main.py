import argparse
import sys
import os

# Add the current directory to sys.path to allow importing from 'src'
sys.path.append(os.getcwd())

from src.engine.search import SearchEngine

def main():
    parser = argparse.ArgumentParser(
        description="Bio-Mapping Engine: Consulta multivectorial de Biodescodificación.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Search Vectors
    parser.add_argument("-s", "--symptom", help="Buscar por nombre de síntoma/dolencia (ej: acné)")
    parser.add_argument("-z", "--zone", help="Buscar por zona del cuerpo (ej: cara, estómago, piel)")
    parser.add_argument("-d", "--description", help="Buscar por palabras clave en la descripción (ej: miedo, separación)")

    # Data path
    parser.add_argument("--data", default="data/processed/processed_data.json", help="Ruta al archivo JSON de datos")

    args = parser.parse_args()

    if not any([args.symptom, args.zone, args.description]):
        parser.print_help()
        sys.exit(1)

    if not os.path.exists(args.data):
        print(f"❌ Error: El archivo de datos no existe en {args.data}")
        sys.exit(1)

    engine = SearchEngine(args.data)

    print("\n" + "="*50)
    print("🧬 BIO-MAPPING ENGINE - RESULTADOS")
    print("="*50 + "\n")

    results = engine.multi_vector_search(
        symptom=args.symptom,
        zone=args.zone,
        description=args.description
    )

    if not results:
        print("⚠️ No se encontraron resultados para los criterios proporcionados.")
        print("Prueba con términos más generales o verifica la ortografía.")
    else:
        print(f"✅ Se encontraron {len(results)} coincidencia(s):\n")
        for i, res in enumerate(results, 1):
            print(f"--- [{i}] {res['sintoma_canonico'].upper()} ---")
            if res['zonas_detectadas']:
                print(f"📍 Zonas: {', '.join(res['zonas_detectadas'])}")
            
            for interp in res['interpretaciones']:
                print(f"\n  👤 Autor: {interp['autor']}")
                if interp['conflicto_emocional']:
                    print(f"  🗯️ Conflicto: {interp['conflicto_emocional']}")
                if interp['modelo_mental']:
                    print(f"  🧠 Modelo: {interp['modelo_mental']}")
                if interp['etapa_biologica']:
                    print(f"  ⏳ Etapa: {interp['etapa_biologica']}")
            print("\n" + "-"*30 + "\n")

    print("="*50)
    print("Nota: Esta herramienta es para fines informativos/educativos.")
    print("No sustituye el consejo médico profesional.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
