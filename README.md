# Water Quality Classification

Real-time water quality classification using SVM, FastAPI, Flutter Web, and Cloudflare Tunnel.

The system classifies water into three categories:

- Clear
- Slightly Turbid
- Turbid

The user opens the project on an iPhone, allows camera access, and the system continuously sends camera frames to the computer for real-time Machine Learning prediction.

---

# 1. System Requirements

Before starting, make sure the computer has:

- Windows 10 or Windows 11
- Python 3.13
- Flutter SDK
- Git (optional)
- Cloudflare Tunnel (`cloudflared`)
- Internet connection
- Visual Studio Code (recommended)

A smartphone is required for real-time camera testing.

Recommended smartphone:

- iPhone with Safari
- Android phone with Chrome

---

# 2. Project Structure

After copying the project, the folder should look like:

```text
Final Project/
│
├── dataset/
│   ├── clear/
│   ├── slightly_turbid/
│   └── turbid/
│
├── dataset_camera/
│   ├── clear/
│   ├── slightly_turbid/
│   └── turbid/
│
├── models/
│   └── water_svm.joblib
│
├── src/
│   ├── features.py
│   ├── train.py
│   ├── evaluate_camera.py
│   └── generate_report.py
│
├── server/
│   ├── main.py
│   └── inference.py
│
├── mobile/
│   ├── lib/
│   │   └── main.dart
│   ├── pubspec.yaml
│   └── build/
│       └── web/
│
├── check_dataset.py
├── start.py
├── requirements.txt
├── README.md
└── qr_code.png