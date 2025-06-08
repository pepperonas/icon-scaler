#!/usr/bin/env python3
"""
Android Icon Generator
Erstellt Android App Icons in verschiedenen Auflösungen aus einem JPG- oder PNG-Bild
"""

import argparse
import os
import sys
from pathlib import Path

from PIL import Image

# Icon-Größen für verschiedene Android-Dichten
ICON_SIZES = {
	'ldpi': 36,
	'mdpi': 48,
	'hdpi': 72,
	'xhdpi': 96,
	'xxhdpi': 144,
	'xxxhdpi': 192
}


def create_android_icons(input_file):
	"""
	Erstellt Android Icons aus einer Bilddatei

	Args:
		input_file: Pfad zur Eingabe-Bilddatei (JPG oder PNG)
	"""
	# Prüfe ob Datei existiert
	if not os.path.exists(input_file):
		print(f"Fehler: Datei '{input_file}' nicht gefunden!")
		return False

	# Prüfe Dateiendung
	valid_extensions = ['.jpg', '.jpeg', '.png']
	file_ext = Path(input_file).suffix.lower()
	if file_ext not in valid_extensions:
		print(f"Fehler: Nur JPG und PNG Dateien werden unterstützt! (gefunden: {file_ext})")
		return False

	# Eingabepfad und -dateiname
	input_path = Path(input_file)
	input_dir = input_path.parent

	# Erstelle Hauptordner "icon"
	icon_dir = input_dir / "icon"
	icon_dir.mkdir(exist_ok=True)

	try:
		# Öffne das Bild
		with Image.open(input_file) as img:
			# Konvertiere zu RGBA für PNG-Unterstützung
			if img.mode not in ('RGB', 'RGBA'):
				img = img.convert('RGBA')

			# Erstelle Icons für jede Dichte
			for density, size in ICON_SIZES.items():
				# Erstelle Unterordner
				density_dir = icon_dir / "res" / f"mipmap-{density}"
				density_dir.mkdir(parents=True, exist_ok=True)

				# Skaliere das Bild
				resized_img = img.resize((size, size), Image.Resampling.LANCZOS)

				# Speichere als PNG
				output_file = density_dir / "ic_launcher.png"
				resized_img.save(output_file, "PNG", optimize=True)

				print(f"✓ Erstellt: {output_file} ({size}x{size}px)")

	except Exception as e:
		print(f"Fehler beim Verarbeiten des Bildes: {e}")
		return False

	print(f"\n✅ Alle Icons wurden erfolgreich in '{icon_dir}' erstellt!")
	return True


def main():
	"""Hauptfunktion"""
	parser = argparse.ArgumentParser(
		description='Erstellt Android App Icons aus einem JPG- oder PNG-Bild'
	)
	parser.add_argument(
		'input_file',
		help='Pfad zur Bilddatei (JPG oder PNG)'
	)

	args = parser.parse_args()

	# Prüfe ob Pillow installiert ist
	try:
		from PIL import Image
	except ImportError:
		print("Fehler: Pillow ist nicht installiert!")
		print("Installiere es mit: pip install Pillow")
		sys.exit(1)

	# Erstelle Icons
	success = create_android_icons(args.input_file)

	if not success:
		sys.exit(1)


if __name__ == "__main__":
	main()
