import argparse
import json
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Asegurar que el path de importación sea correcto para el paquete
try:
    from src.engine.search import SearchEngine
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from src.engine.search import SearchEngine

console = Console()

class CLIHandler:
    def __init__(self, engine: SearchEngine):
        self.engine = engine

    def handle(self, args: argparse.Namespace):
        # Ejecutamos la búsqueda multi-vectorial
        results = self.engine.multi_vector_search(
            symptom=args.symptom,
            zone=args.zone,
            description=args.description
        )

        if not results:
            console.print("[yellow]⚠ No se encontraron coincidencias para los criterios especificados.[/yellow]")
            return

        # Determinamos si estamos en modo "Búsqueda de Contenido" (Description)
        is_content_search = args.description is not None
        self._display_results(results, args.description, is_content_search)

    def _display_results(self, results: list[dict], query: str = None, content_mode: bool = False):
        console.print(f"\n[bold green]✅ {len(results)} coincidencia(s) encontrada(s):[/bold green]\n")
        
        for idx, item in enumerate(results, 1):
            symptom_name = item.get("sintoma_canonico", "Desconocido")
            zones = ", ".join(item.get("zonas_detectadas", []))
            
            # Construcción del encabezado del Panel
            if content_mode:
                # Si buscamos texto, aclaramos que el síntoma es solo el contenedor del match
                title = f"Coincidencia de texto en: {symptom_name}"
                header_text = f"[bold cyan]Contenido relacionado con:[/bold cyan] {query}\n"
                header_text += f"[dim]Contexto: {symptom_name} ({zones})[/dim]\n"
            else:
                # Búsqueda clásica por síntoma o zona
                title = f"Registro: {symptom_name}"
                header_text = f"[bold cyan]Síntoma:[/bold cyan] {symptom_name}\n"
                header_text += f"[bold magenta]Zonas:[/bold magenta] {zones}\n"

            panel_content = Text()
            panel_content.append(header_text)
            panel_content.append("\n[bold yellow]Interpretaciones relevantes:[/bold yellow]\n")

            interpretations = item.get("interpretaciones", [])
            
            # Filtro de granularidad: Si hay una query de texto, solo mostramos la interpretación que coincide
            if query:
                q = query.lower()
                interpretations = [
                    i for i in interpretations 
                    if q in i.get("conflicto_emocional", "").lower() or 
                       q in i.get("modelo_mental", "").lower()
                ]

            if not interpretations:
                panel_content.append("  (Sin interpretaciones que coincidan con el texto)\n")
            else:
                for interp in interpretations:
                    author = interp.get("autor", "N/A")
                    conflicto = interp.get("conflicto_emocional", "N/A")
                    modelo = interp.get("modelo_mental", "N/A")
                    etapa = interp.get("etapa_biologica", "N/A")

                    # Añadimos la interpretación con un formato limpio
                    panel_content.append(f"  • [bold white]Autor:[/bold white] {author}\n")
                    panel_content.append(f"    [italic]Conflicto:[/italic] {conflicto}\n")
                    if modelo:
                        panel_content.append(f"    [italic]Modelo:[/italic] {modelo}\n")
                    if etapa:
                        panel_content.append(f"    [italic]Etapa:[/italic] {etapa}\n")
                    panel_content.append("  " + "-"*30 + "\n")

            console.print(Panel(panel_content, title=title, expand=False))

def main():
    parser = argparse.ArgumentParser(description="Bio-Mapping Engine CLI")
    parser.add_argument("--symptom", help="Buscar por nombre de síntoma (ej: acné)")
    parser.add_argument("--zone", help="Buscar por zona física (ej: cara)")
    parser.add_argument("--description", help="Buscar texto en conflictos o modelos (ej: auto-estima)")

    args = parser.parse_args()

    # Ruta absoluta al dataset basado en la raíz del proyecto
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    data_path = os.path.join(base_dir, "data", "processed", "processed_data.json")

    if not os.path.exists(data_path):
        console.print(f"[bold red]❌ Error: No se encontró el archivo en {data_path}[/bold red]")
        return

    engine = SearchEngine(data_path)
    handler = CLIHandler(engine)
    handler.handle(args)

if __name__ == "__main__":
    main()
