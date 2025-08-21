from pathlib import Path
import pandas as pd

# Ruta raíz del dataset
ROOT = Path("data/raw")

# Ruta para guardar el csv
OUTPUT_DIR = Path("data/dataframe")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # crea la carpeta si no existe
OUTPUT_FILE = OUTPUT_DIR / "dataset.csv"

# Carpetas (clases)
CLASSES = ["COVID", "Lung_Opacity", "Normal", "Viral Pneumonia"]

rows = []
for cls in CLASSES:
    img_dir = ROOT / cls / "images"   # ahora buscamos dentro de 'images'
    if img_dir.exists():
        for img in img_dir.glob("*.*"):
            if img.suffix.lower() in [".png", ".jpg", ".jpeg"]:  # extensiones permitidas
                rows.append({
                    # ruta relativa desde la carpeta raíz del proyecto
                    "img_path": str(img.relative_to(".")),  
                    "label": cls
                })

# Crear DataFrame
df = pd.DataFrame(rows)

# Guardar a CSV en la ruta especificada
df.to_csv(OUTPUT_FILE, index=False)

print(f"Total imágenes: {len(df)}")
print(f"Archivo CSV guardado en: {OUTPUT_FILE}")
