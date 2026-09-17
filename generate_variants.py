"""
Genera variantes únicas de cada PDF en ./pdfs, modificando un campo de
metadata (para que el checksum SHA-256 cambie), y las guarda en
./pdfs_variants. Requiere pypdf (ya es dependencia del proyecto).

Recorta los PDFs a un máximo de páginas para acelerar la generación,
la transferencia de red y el procesamiento del servidor durante la
prueba de carga.

Uso:
    uv run python generate_variants.py
"""
import uuid
from pathlib import Path
from pypdf import PdfReader, PdfWriter

SOURCE_DIR = Path("pdfs")
OUTPUT_DIR = Path("pdfs_variants")
VARIANTS_PER_FILE = 60
MAX_PAGES = 2  # recorte para acelerar generación, red y extracción

OUTPUT_DIR.mkdir(exist_ok=True)

source_files = sorted(SOURCE_DIR.glob("*.pdf"))
if not source_files:
    raise SystemExit(f"No se encontraron PDFs en {SOURCE_DIR.resolve()}")

generated = []

for source in source_files:
    base_reader = PdfReader(str(source))
    pages_to_use = base_reader.pages[:MAX_PAGES]

    for i in range(VARIANTS_PER_FILE):
        writer = PdfWriter()
        for page in pages_to_use:
            writer.add_page(page)

        writer.add_metadata({"/SpikeTestId": str(uuid.uuid4())})

        out_name = f"{source.stem}_v{i}.pdf"
        out_path = OUTPUT_DIR / out_name
        with open(out_path, "wb") as f:
            writer.write(f)

        generated.append(out_name)

print(f"Total generado: {len(generated)} archivos en {OUTPUT_DIR.resolve()}")
