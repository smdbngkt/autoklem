import subprocess
import json
import requests
import time
from colorama import init, Fore, Style

# Inisialisasi colorama
init()

# Fungsi untuk mengambil alamat wallet dari perintah shell
def get_wallet_address():
    command = "$HOME/nubit-node/bin/nubit state account-address --node.store $HOME/.nubit-light-nubit-alphatestnet-1"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Mengambil hasil dari perintah
    output = result.stdout
    data = json.loads(output)

    # Memastikan hasilnya tidak kosong
    if "result" in data and data["result"]:
        return data["result"]
    else:
        print("Gagal mengambil alamat wallet.")
        return None

# Fungsi untuk mengirim permintaan ke API faucet
def send_request(wallet):
    url = 'https://faucet.nubit.org/api/v1/faucet/give_me'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'id,en;q=0.9,jv;q=0.8',
        'Content-Type': 'application/json',
        'Origin': 'https://faucet.nubit.org',
        'Referer': 'https://faucet.nubit.org/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    payload = {
        "address": wallet,
        "chainId": "nubit-alphatestnet-1"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=180)
        response.raise_for_status()
        if response.status_code == 200:
            print(f"{Fore.GREEN}Permintaan berhasil untuk wallet {wallet}:{Style.RESET_ALL}")
            print(response.json())
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Permintaan dengan wallet {wallet} gagal: {e}{Style.RESET_ALL}")
    return None

if __name__ == "__main__":
    # Loop utama untuk menjalankan script setiap 24 jam 30 menit
    while True:
        # Mengambil alamat wallet
        wallet_address = get_wallet_address()

        if wallet_address:
            print(f"Wallet Address: {wallet_address}")
            # Mengirim permintaan ke API faucet dengan wallet yang diambil
            send_request(wallet_address)
        else:
            print("Tidak ada wallet address yang ditemukan.")

        # Tunggu 24 jam 30 menit (90 menit) sebelum menjalankan kembali
        time.sleep(90 * 60)  # Menunggu 90 menit sebelum dijalankan lagi
