# androidicon

Ein Python-Tool zur automatischen Generierung von Android App Icons in allen erforderlichen Auflösungen.

## Features

- ✅ Unterstützt JPG und PNG Dateien
- ✅ Behält PNG-Transparenz bei
- ✅ Erstellt alle Android mipmap-Auflösungen automatisch
- ✅ Optimierte PNG-Ausgabe
- ✅ Einfache Command-Line-Nutzung

## Installation

### Voraussetzungen

- Python 3.6+
- Pillow

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt
```

### Tool installieren

```bash
# Repository klonen oder Datei herunterladen
chmod +x androidicon.py

# Optional: Systemweit installieren
sudo cp androidicon.py /usr/local/bin/androidicon
```

## Verwendung

```bash
# Mit Python
python androidicon.py icon.png

# Oder wenn systemweit installiert
androidicon icon.jpg
```

## Ausgabe

Das Tool erstellt folgende Ordnerstruktur im gleichen Verzeichnis wie die Eingabedatei:

```
icon/
└── res/
    ├── mipmap-ldpi/
    │   └── ic_launcher.png (36x36)
    ├── mipmap-mdpi/
    │   └── ic_launcher.png (48x48)
    ├── mipmap-hdpi/
    │   └── ic_launcher.png (72x72)
    ├── mipmap-xhdpi/
    │   └── ic_launcher.png (96x96)
    ├── mipmap-xxhdpi/
    │   └── ic_launcher.png (144x144)
    └── mipmap-xxxhdpi/
        └── ic_launcher.png (192x192)
```

## Icon-Größen

| Dichte  | Größe      | Verwendung                          |
|---------|------------|-------------------------------------|
| ldpi    | 36x36 px   | Alte Geräte mit niedriger Auflösung |
| mdpi    | 48x48 px   | Basis-Auflösung                     |
| hdpi    | 72x72 px   | HD-Geräte                           |
| xhdpi   | 96x96 px   | Extra HD                            |
| xxhdpi  | 144x144 px | Full HD                             |
| xxxhdpi | 192x192 px | 4K Geräte                           |

## Beispiel

```bash
$ androidicon logo.png
✓ Erstellt: icon/res/mipmap-ldpi/ic_launcher.png (36x36px)
✓ Erstellt: icon/res/mipmap-mdpi/ic_launcher.png (48x48px)
✓ Erstellt: icon/res/mipmap-hdpi/ic_launcher.png (72x72px)
✓ Erstellt: icon/res/mipmap-xhdpi/ic_launcher.png (96x96px)
✓ Erstellt: icon/res/mipmap-xxhdpi/ic_launcher.png (144x144px)
✓ Erstellt: icon/res/mipmap-xxxhdpi/ic_launcher.png (192x192px)

✅ Alle Icons wurden erfolgreich in 'icon' erstellt!
```

## Lizenz

MIT License

Copyright (c) 2025 Martin Pfeffer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Autor

**Martin Pfeffer** - 2025

## Beiträge

Pull Requests sind willkommen! Für größere Änderungen bitte erst ein Issue erstellen.