import os
import socket
import subprocess
import platform
from ipwhois import IPWhois

# Configurações
host_alvo = "8.8.8.8"  # Google DNS
quantidade_pings = "1"  # Você pode aumentar isso se quiser mais precisão

def verificar_ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    comando = ["ping", param, quantidade_pings, host]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode == 0:
            print("✅ Rede ONLINE")
            # Extrai latência (isso é meio gambi mas funciona pra maioria)
            if platform.system().lower() == "windows":
                for linha in resultado.stdout.splitlines():
                    if "tempo" in linha.lower():
                        print(f"📡 {linha.strip()}")
            else:
                for linha in resultado.stdout.splitlines():
                    if "time=" in linha:
                        print(f"📡 {linha.strip()}")
        else:
            print("❌ Rede OFFLINE")
    except Exception as e:
        print(f"Erro ao executar o ping: {e}")

def obter_info_host():
    try:
        nome_host = socket.gethostname()
        ip_local = socket.gethostbyname(nome_host)

        print(f"🖥️ Hostname: {nome_host}")
        print(f"📍 IP Local: {ip_local}")

        # WHOIS do IP alvo (se quiser info do IP local, usa IP externo)
        obj = IPWhois(host_alvo)
        whois_info = obj.lookup_rdap()
        print(f"🌍 Provedor: {whois_info['network']['name']}")
        print(f"📌 País: {whois_info['network']['country']}")
        print(f"🔗 Org: {whois_info['network']['remarks'][0]['description'] if whois_info['network'].get('remarks') else 'N/A'}")

    except Exception as e:
        print(f"Erro ao obter informações do host: {e}")

# Execução
print("📡 Iniciando monitoramento de rede...\n")
verificar_ping(host_alvo)
print()
obter_info_host()
