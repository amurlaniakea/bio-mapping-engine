import os
import requests
import json
import sys

# Configuración
PROJECT_KEY = "bio-mapping-motor"
ORGANIZATION = "amurlaniakea"
SONAR_TOKEN = os.getenv("SONAR_TOKEN")
BASE_URL = f"https://sonarcloud.io/api"

def check_sonar_issues():
    if not SONAR_TOKEN:
        print("ERROR: SONAR_TOKEN no encontrado en las variables de entorno.")
        return 1

    print(f"🔍 Iniciando vigilancia de calidad para: {PROJECT_KEY}...")
    
    # Endpoint para buscar problemas no resueltos
    # Filtramos por severidad para priorizar lo crítico
    url = f"{BASE_URL}/issues/search"
    params = {
        "componentKeys": PROJECT_KEY,
        "resolved": "false",
        "ps": 50  # Traer hasta 50 problemas
    }
    
    try:
        response = requests.get(url, params=params, auth=(SONAR_TOKEN, ""))
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Error conectando con SonarCloud: {e}")
        return 1

    issues = data.get("issues", [])
    total_issues = data.get("total", 0)

    if total_issues == 0:
        print("✅ ¡Calidad perfecta! No se han detectado problemas pendientes.")
        return 0
    
    print(f"⚠️ Se han detectado {total_issues} problemas pendientes.")
    print("-" * 40)

    # Clasificación de hallazgos
    summary = {"CRITICAL": 0, "MAJOR": 0, "MINOR": 0, "INFO": 0}
    
    for issue in issues:
        severity = issue.get("severity", "INFO")
        summary[severity] = summary.get(severity, 0) + 1
        
        # Imprimir un resumen de los más críticos
        if severity in ["CRITICAL", "MAJOR"]:
            file = issue.get("component", "Unknown file").split(":")[-1]
            line = issue.get("line", "N/A")
            msg = issue.get("message", "No message")
            print(f"[{severity}] {file}:{line} -> {msg}")

    print("-" * 40)
    print(f"Resumen de severidad: {summary}")
    print("-" * 40)

    # Retornamos 1 si hay problemas críticos o mayores para disparar la acción
    if summary.get("CRITICAL", 0) > 0 or summary.get("MAJOR", 0) > 0:
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = check_sonar_issues()
    sys.exit(exit_code)
