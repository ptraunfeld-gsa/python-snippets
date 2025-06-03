from pdfid import pdfid
from pathlib import Path
import json
from tabulate import tabulate

def scan_pdf(pdf_path: Path):
    if not pdf_path.exists():
        raise ValueError(f"{pdf_path} does not exist")
    options = pdfid.get_fake_options()
    options.scan = True
    options.json = True
    results = pdfid.PDFiDMain([f"{pdf_path}"], options)
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("More args, please")
        sys.exit(1)
    results = scan_pdf(Path(sys.argv[1]))
    if 'reports' in results and len(results['reports']) > 0:
        print(tabulate([[k,v] for k,v in results['reports'][0].items()]))
    else:
        print(json.dumps(results, indent=2))