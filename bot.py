import os
import requests
import time
import random
import re
from bs4 import BeautifulSoup
from rich import print, box
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from textwrap import wrap
from datetime import datetime

console = Console()
BASE_GM = "https://api.guerrillamail.com/ajax.php"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header():
    console.print("[#7f1d1d]─────▄████▀█▄[/]")
    console.print("[#b91c1c]───▄█████████████████▄[/]")
    console.print("[#dc2626]─▄█████.▼.▼.▼.▼.▼.▼▼▼▼[/]")
    console.print("[#ef4444]▄███████▄.▲.▲▲▲▲▲▲▲▲[/]")
    console.print("[#f87171]████████████████████▀▀[/]")
    console.print("[bold bright_black]" + "━" * 55 + "[/bold bright_black]")
    tanggal = datetime.now().strftime("%A, %d %B %Y")
    try:
        ip = requests.get("https://ifconfig.me", timeout=5).text.strip()
    except:
        ip = "Tidak terdeteksi"
    console.print("[bold cyan][📧] VERIFMAIL BY KAYDENZO[/bold cyan]")
    console.print(f"[bold bright_blue][📅] Tanggal:[/] {tanggal}")
    console.print(f"[bold bright_blue][🌐] IP Publik:[/] {ip}")
    console.print("[bold bright_black]" + "━" * 55 + "[/bold bright_black]")

def proses_verifikasi(html, pengirim=None, subjek="-"):
    soup = BeautifulSoup(html, "html.parser")
    hasil_output = ""

    text = soup.get_text(separator="\n").strip()
    baris = [b.strip() for b in text.splitlines() if b.strip()]

    hasil_output += f"\n[bold cyan]📩 INFORMASI EMAIL:[/bold cyan]\n"
    hasil_output += f"[bold blue]Pengirim :[/bold blue] {pengirim or '-'}\n"
    hasil_output += f"[bold blue]Subjek   :[/bold blue] {subjek or '-'}\n"

    hasil_output += f"\n[bold cyan]📨 PREVIEW EMAIL:[/bold cyan]\n"
    for line in baris[:20]:
        for wrapped in wrap(line, width=90):
            hasil_output += wrapped + "\n"

    hasil_output += "\n"  # Spasi kosong sebelum info link/OTP

    # Coba deteksi tombol/link verifikasi
    link = soup.find("a", string=re.compile("verifikasi", re.I))
    if not link:
        all_links = soup.find_all("a", href=True)
        for l in all_links:
            if "verif" in l.get("href").lower() or "confirm" in l.get("href").lower():
                link = l
                break

    if link and link.get("href"):
        href = link.get("href")
        hasil_output += f"[bold cyan]🔗 Link verifikasi ditemukan:[/bold cyan] [blue underline]{href}[/blue underline]\n"
        try:
            r = requests.get(href, timeout=10)
            if r.status_code == 200:
                return True, hasil_output + "[green]✅ Verifikasi berhasil![/green]\n"
        except:
            hasil_output += "[red]❌ Gagal membuka link verifikasi.[/red]\n"

    otp = re.findall(r"\b\d{4,8}\b", text)
    if otp:
        hasil_output += f"[yellow]🔐 OTP ditemukan:[/yellow] [bold]{otp[0]}[/bold]\n"
    else:
        hasil_output += "[red]⚠️ Tidak ada link atau OTP terdeteksi.[/red]\n"

    return False, hasil_output

def email_mail_tm():
    r = requests.get("https://api.mail.tm/domains")
    domain = r.json()["hydra:member"][0]["domain"]
    user = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=10))
    email = f"{user}@{domain}"
    pw = "12345678"
    requests.post("https://api.mail.tm/accounts", json={"address": email, "password": pw})
    token = requests.post("https://api.mail.tm/token", json={"address": email, "password": pw}).json()
    return email, {"Authorization": f"Bearer {token['token']}"}

def tunggu_mail_tm(headers):
    for _ in range(60):
        res = requests.get("https://api.mail.tm/messages", headers=headers).json()
        msgs = res.get("hydra:member", [])
        if msgs:
            msg = msgs[0]
            detail = requests.get(f"https://api.mail.tm/messages/{msg['id']}", headers=headers).json()
            isi = detail.get("html", [detail.get("text", "")])[0]
            pengirim = detail.get("from", {}).get("address")
            subjek = detail.get("subject", "-")
            return proses_verifikasi(isi, pengirim, subjek)
        time.sleep(1)
    return False, "[red]❌ Tidak ada email masuk (mail.tm)[/red]"

def email_mail_gw():
    r = requests.get("https://api.mail.gw/domains")
    domain = r.json()["hydra:member"][0]["domain"]
    user = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=10))
    email = f"{user}@{domain}"
    pw = "12345678"
    requests.post("https://api.mail.gw/accounts", json={"address": email, "password": pw})
    token = requests.post("https://api.mail.gw/token", json={"address": email, "password": pw}).json()
    return email, {"Authorization": f"Bearer {token['token']}"}

def tunggu_mail_gw(headers):
    for _ in range(60):
        res = requests.get("https://api.mail.gw/messages", headers=headers).json()
        msgs = res.get("hydra:member", [])
        if msgs:
            msg = msgs[0]
            detail = requests.get(f"https://api.mail.gw/messages/{msg['id']}", headers=headers).json()
            isi = detail.get("html", [detail.get("text", "")])[0]
            pengirim = detail.get("from", {}).get("address")
            subjek = detail.get("subject", "-")
            return proses_verifikasi(isi, pengirim, subjek)
        time.sleep(1)
    return False, "[red]❌ Tidak ada email masuk (mail.gw)[/red]"

def email_guerrillamail():
    r = requests.get(f"{BASE_GM}?f=get_email_address").json()
    return r["email_addr"], r["sid_token"]

def tunggu_guerrillamail(sid):
    seen_ids = set()
    for _ in range(60):
        r = requests.get(BASE_GM, params={"f": "check_email", "seq": 0, "sid_token": sid}).json()
        msgs = r.get("list", [])
        for msg in msgs:
            if msg["mail_id"] in seen_ids:
                continue
            seen_ids.add(msg["mail_id"])
            if "welcome" in msg["mail_subject"].lower():
                continue
            detail = requests.get(BASE_GM, params={"f": "fetch_email", "sid_token": sid, "email_id": msg["mail_id"]}).json()
            isi = detail.get("mail_body", "")
            pengirim = msg.get("mail_from", "-")
            subjek = msg.get("mail_subject", "-")
            return proses_verifikasi(isi, pengirim, subjek)
        time.sleep(1)
    return False, "[red]❌ Tidak ada email masuk (GuerrillaMail)[/red]"

def email_mailnesia():
    user = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=10))
    return f"{user}@mailnesia.com", user

def tunggu_mailnesia(username):
    for _ in range(60):
        r = requests.get(f"https://mailnesia.com/mailbox/{username}")
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.select("tr.emailheader")
        for row in rows:
            if "welcome" in row.text.lower():
                continue
            email_id = row.get("id")
            pengirim = row.select_one("td:nth-of-type(2)").text.strip()
            subjek = row.select_one("td:nth-of-type(3)").text.strip()
            detail_url = f"https://mailnesia.com/mailbox/{username}/{email_id}"
            r = requests.get(detail_url)
            soup2 = BeautifulSoup(r.text, "html.parser")
            html = soup2.select_one(f"#text_html_{email_id}") or soup2.select_one(f"#text_plain_{email_id}")
            isi = html.get_text(separator="\n").strip() if html else ""
            return proses_verifikasi(isi, pengirim, subjek)
        time.sleep(1)
    return False, "[red]❌ Tidak ada email masuk (mailnesia)[/red]"

def tampilkan_status(layanan, status):
    table = Table(box=box.HEAVY_HEAD, show_header=True, header_style="bold white", expand=False)
    table.add_column("No", justify="center", style="cyan", width=5)
    table.add_column("Service", justify="left", style="bold cyan", width=25)
    table.add_column("Status", justify="center", style="green", width=15)
    for i, (name, _, _) in enumerate(layanan):
        st, *_ = status[i]
        symbol = "✅ Aktif" if st == "Aktif" else "❌ Tidak Aktif"
        table.add_row(str(i + 1), name, symbol)
    console.print(table)

def main():
    while True:
        clear()
        header()
        layanan = [
            ("mail.tm", email_mail_tm, tunggu_mail_tm),
            ("mail.gw", email_mail_gw, tunggu_mail_gw),
            ("GuerrillaMail", email_guerrillamail, tunggu_guerrillamail),
            ("Mailnesia", email_mailnesia, tunggu_mailnesia),
        ]
        status = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("🔍 Mengecek layanan...", total=None)
            for _, func, wait_func in layanan:
                try:
                    data = func()
                    status.append(("Aktif", data, wait_func))
                except:
                    status.append(("Tidak Aktif", None, wait_func))
            progress.remove_task(task)

        tampilkan_status(layanan, status)
        pilihan = Prompt.ask("\n👉 Pilih layanan (1-4) atau 5 untuk keluar", choices=["1", "2", "3", "4", "5"])
        if pilihan == "5":
            console.print("\n[red]🚪 Keluar...[/red]")
            break

        idx = int(pilihan) - 1
        aktif, data, tunggu = status[idx]
        name, gen_func, _ = layanan[idx]

        if not data:
            console.print("[yellow]↪ Layanan tidak aktif, mencoba generate email...[/yellow]")
            try:
                data = gen_func()
            except:
                console.print("[red]❌ Gagal generate, kembali ke menu.[/red]")
                input("Tekan ENTER...")
                continue

        console.print()
        email, headers = data
        console.print(f"[green]✅ Gunakan email:[/green] [bold]{email}[/bold]")
        input("🔄 Tekan ENTER setelah digunakan...")

        with Progress(
            SpinnerColumn(),
            TextColumn(f"[progress.description]📬 Menunggu email masuk dari {name}..."),
            transient=True,
        ) as progress:
            task = progress.add_task("", total=None)
            status_result, output_text = tunggu(headers if isinstance(headers, dict) else headers)
            progress.remove_task(task)

        console.print(output_text)
        if status_result is True:
            console.print("[green]✅ Verifikasi berhasil![/green]")

        input("\n🔁 Tekan ENTER untuk kembali ke menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]❌ Dihentikan oleh pengguna.[/red]")
