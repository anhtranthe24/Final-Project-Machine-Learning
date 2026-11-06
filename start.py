import os
import re
import sys
import time
import subprocess
import threading
import webbrowser

import qrcode


PROJECT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CLOUDFLARED = (
    r"C:\Program Files (x86)\cloudflared\cloudflared.exe"
)

LOCAL_URL = "http://127.0.0.1:8000"

QR_PATH = os.path.join(
    PROJECT_DIR,
    "qr_code.png"
)


def start_fastapi():
    print("Starting FastAPI...")

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "server.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000"
        ],
        cwd=PROJECT_DIR
    )

    time.sleep(3)

    if process.poll() is not None:
        raise RuntimeError(
            "FastAPI failed to start."
        )

    print("FastAPI started.")
    return process


def start_cloudflare():
    print("Starting Cloudflare Tunnel...")

    process = subprocess.Popen(
        [
            CLOUDFLARED,
            "tunnel",
            "--url",
            LOCAL_URL
        ],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    return process


def create_qr(url):
    qr = qrcode.QRCode(
        version=1,
        box_size=12,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image()

    image.save(QR_PATH)

    print(f"QR code saved: {QR_PATH}")

    webbrowser.open(
        "file:///" +
        QR_PATH.replace("\\", "/")
    )


def main():
    if not os.path.exists(CLOUDFLARED):
        raise FileNotFoundError(
            f"Không tìm thấy cloudflared:\n{CLOUDFLARED}"
        )

    fastapi = None
    cloudflare = None

    try:
        fastapi = start_fastapi()

        cloudflare = start_cloudflare()

        public_url = None

        print()
        print("Waiting for Cloudflare URL...")
        print()

        start_time = time.time()

        while time.time() - start_time < 30:

            line = cloudflare.stdout.readline()

            if not line:
                time.sleep(0.1)
                continue

            print(
                "[cloudflare]",
                line.strip()
            )

            match = re.search(
                r"https://[a-zA-Z0-9-]+\.trycloudflare\.com",
                line
            )

            if match:
                public_url = match.group(0)
                break

        if not public_url:
            raise RuntimeError(
                "Không lấy được Cloudflare URL."
            )

        print()
        print("=" * 50)
        print("PUBLIC URL")
        print(public_url)
        print("=" * 50)
        print()

        create_qr(public_url)

        print("Scan QR bằng iPhone để mở project.")
        print("Không được đóng cửa sổ này.")
        print()

        while True:
            if fastapi.poll() is not None:
                print("FastAPI stopped.")
                break

            if cloudflare.poll() is not None:
                print("Cloudflare Tunnel stopped.")
                break

            time.sleep(1)

    except KeyboardInterrupt:
        print()
        print("Stopping...")

    finally:
        if cloudflare is not None:
            cloudflare.terminate()

        if fastapi is not None:
            fastapi.terminate()

        print("All services stopped.")


if __name__ == "__main__":
    main()