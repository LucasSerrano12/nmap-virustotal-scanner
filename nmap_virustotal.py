
import subprocess
import re
import requests

# =============================================
# Nmap + VirusTotal Scanner
# Escanea una red con Nmap y analiza las IPs
# encontradas en VirusTotal automáticamente.
# =============================================

API_KEY = "TU_API_KEY"

def escanear_red(objetivo):
    print(f"\n[*] Escaneando {objetivo} con Nmap...")
    resultado = subprocess.run(
        ["nmap", "-sn", objetivo],
        capture_output=True,
        text=True
    )
    return resultado.stdout

def extraer_ips(output_nmap):
    ips = re.findall(r'\d+\.\d+\.\d+\.\d+', output_nmap)
    return ips

def analizar_ip(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": API_KEY}

    respuesta = requests.get(url, headers=headers)

    if respuesta.status_code != 200:
        print(f"  [!] Error consultando {ip}")
        return

    datos = respuesta.json()
    atributos = datos["data"]["attributes"]
    estadisticas = atributos["last_analysis_stats"]

    maliciosos = estadisticas["malicious"]
    sospechosos = estadisticas["suspicious"]
    pais = atributos.get("country", "Desconocido")
    reputacion = atributos.get("reputation", 0)

    if maliciosos > 0:
        veredicto = f"⚠️  MALICIOSA ({maliciosos} motores)"
    elif sospechosos > 0:
        veredicto = f"🟡 SOSPECHOSA ({sospechosos} motores)"
    else:
        veredicto = "✅ LIMPIA"

    print(f"  IP:          {ip}")
    print(f"  País:        {pais}")
    print(f"  Reputación:  {reputacion}")
    print(f"  Veredicto:   {veredicto}")
    print(f"  Reporte:     https://www.virustotal.com/gui/ip-address/{ip}")
    print(f"  {'-'*45}")

# =============================================
# Programa principal
# =============================================

if __name__ == "__main__":
    print("=== Nmap + VirusTotal Scanner ===")
    objetivo = input("\nIngresá IP o rango a escanear (ej: 192.168.1.0/24): ").strip()

    output_nmap = escanear_red(objetivo)
    ips = extraer_ips(output_nmap)

    if not ips:
        print("[!] No se encontraron IPs.")
    else:
        print(f"\n[*] Se encontraron {len(ips)} IPs. Analizando en VirusTotal...\n")
        print("=" * 50)
        for ip in ips:
            analizar_ip(ip)

    print("\n[*] Análisis completado.")
