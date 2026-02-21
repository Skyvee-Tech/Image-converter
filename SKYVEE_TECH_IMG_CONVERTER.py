import os
import time
import sys
from pathlib import Path

try:
    from PIL import Image
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Install dulu: pip install Pillow colorama")
    sys.exit(1)

G = Fore.GREEN
R = Fore.RED
Y = Fore.YELLOW
C = Fore.CYAN
W = Fore.WHITE
M = Fore.MAGENTA
RESET = Style.RESET_ALL

SUPPORTED_INPUT  = ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.tif', '.gif', '.ico']
SUPPORTED_OUTPUT = ['jpg', 'jpeg', 'png', 'bmp', 'webp', 'tiff', 'ico', 'gif']

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def header():
    clear()
    print(G + """
  ================================================================

         SKYVEE TECH - IMAGE CONVERTER v1.0
         Convert any image to any format

  ================================================================
    """ + RESET)

def format_size(b):
    if b < 1024:
        return f"{b} B"
    elif b < 1024 * 1024:
        return f"{b/1024:.1f} KB"
    else:
        return f"{b/(1024*1024):.2f} MB"

def convert_image(src_path, target_format, output_folder):
    src_path = Path(src_path)
    size_before = src_path.stat().st_size

    img = Image.open(src_path)
    target_format = target_format.lower().strip('.')

    # Handle ICO - butuh ukuran spesifik
    if target_format == 'ico':
        img = img.convert('RGBA')
        img = img.resize((256, 256), Image.LANCZOS)
        out_path = Path(output_folder) / (src_path.stem + '.ico')
        img.save(out_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

    # Handle GIF
    elif target_format == 'gif':
        img = img.convert('P', palette=Image.ADAPTIVE)
        out_path = Path(output_folder) / (src_path.stem + '.gif')
        img.save(out_path, format='GIF')

    # Handle JPG/JPEG - ga support alpha channel
    elif target_format in ['jpg', 'jpeg']:
        if img.mode in ('RGBA', 'P', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        out_path = Path(output_folder) / (src_path.stem + '.jpg')
        img.save(out_path, format='JPEG', quality=95, optimize=True)

    # Format lain (PNG, BMP, WEBP, TIFF)
    else:
        if target_format == 'png':
            img = img.convert('RGBA') if img.mode not in ('RGBA', 'RGB') else img
        elif target_format in ['bmp', 'tiff']:
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
        elif target_format == 'webp':
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')

        out_path = Path(output_folder) / (src_path.stem + f'.{target_format}')
        img.save(out_path, format=target_format.upper())

    size_after = out_path.stat().st_size
    return size_before, size_after, str(out_path)

def convert_single():
    header()
    print(W + "  Format yang didukung:" + RESET)
    print(C + f"  Input  : {', '.join(SUPPORTED_INPUT)}" + RESET)
    print(C + f"  Output : {', '.join(SUPPORTED_OUTPUT)}" + RESET)
    print()

    filepath = input(C + "  [?] Path file    : " + RESET).strip().strip('"')

    if not Path(filepath).exists():
        print(R + "\n  [-] File tidak ditemukan!" + RESET)
        return

    if Path(filepath).suffix.lower() not in SUPPORTED_INPUT:
        print(R + f"\n  [-] Format input tidak didukung!" + RESET)
        return

    print()
    print(W + "  Pilih format output:")
    for i, fmt in enumerate(SUPPORTED_OUTPUT, 1):
        print(W + f"  [{i}]  {fmt.upper()}")

    choice = input(G + "\n  [?] Choose: " + RESET).strip()
    try:
        target_format = SUPPORTED_OUTPUT[int(choice) - 1]
    except:
        print(R + "  [-] Pilihan tidak valid!" + RESET)
        return

    output_folder = str(Path(filepath).parent / "converted")
    os.makedirs(output_folder, exist_ok=True)

    print(Y + "\n  [*] Converting..." + RESET)

    try:
        size_before, size_after, out_path = convert_image(filepath, target_format, output_folder)
        print(G + f"\n  [+] Berhasil!" + RESET)
        print(W + f"  File          : {Path(filepath).name}")
        print(W + f"  Format asal   : {Path(filepath).suffix.upper().strip('.')}")
        print(W + f"  Format baru   : {target_format.upper()}")
        print(W + f"  Size sebelum  : {format_size(size_before)}")
        print(W + f"  Size sesudah  : {format_size(size_after)}")
        print(G + f"  Output        : {out_path}" + RESET)
    except Exception as e:
        print(R + f"\n  [-] Error: {e}" + RESET)

def convert_folder():
    header()
    print(W + "  Format yang didukung:" + RESET)
    print(C + f"  Input  : {', '.join(SUPPORTED_INPUT)}" + RESET)
    print(C + f"  Output : {', '.join(SUPPORTED_OUTPUT)}" + RESET)
    print()

    folderpath = input(C + "  [?] Path folder  : " + RESET).strip().strip('"')

    if not Path(folderpath).exists():
        print(R + "\n  [-] Folder tidak ditemukan!" + RESET)
        return

    files = [f for f in Path(folderpath).iterdir() if f.suffix.lower() in SUPPORTED_INPUT]

    if not files:
        print(Y + "\n  [!] Tidak ada foto yang didukung di folder ini." + RESET)
        return

    print()
    print(W + "  Pilih format output:")
    for i, fmt in enumerate(SUPPORTED_OUTPUT, 1):
        print(W + f"  [{i}]  {fmt.upper()}")

    choice = input(G + "\n  [?] Choose: " + RESET).strip()
    try:
        target_format = SUPPORTED_OUTPUT[int(choice) - 1]
    except:
        print(R + "  [-] Pilihan tidak valid!" + RESET)
        return

    output_folder = str(Path(folderpath) / "converted")
    os.makedirs(output_folder, exist_ok=True)

    print(G + f"\n  [*] Ditemukan {len(files)} foto. Converting...\n" + RESET)
    print(G + f"  {'No':<4} {'Filename':<35} {'From':<8} {'To':<8} {'Size After'}" + RESET)
    print(G + "  " + "─"*65 + RESET)

    success = 0
    failed = 0

    for i, fp in enumerate(files, 1):
        try:
            sb, sa, out = convert_image(fp, target_format, output_folder)
            print(G + f"  {i:<4} {fp.name:<35} {fp.suffix.strip('.'):<8} {target_format:<8} {format_size(sa)}" + RESET)
            success += 1
        except Exception as e:
            print(R + f"  {i:<4} {fp.name:<35} ERROR: {str(e)[:30]}" + RESET)
            failed += 1

    print(G + "\n  " + "─"*65 + RESET)
    print(G + f"\n  [+] Selesai! Berhasil: {success} | Gagal: {failed}" + RESET)
    print(G + f"  [+] Output disimpan di: {output_folder}" + RESET)

def menu():
    while True:
        header()
        print(W + "  [1]  Convert 1 File")
        print(W + "  [2]  Convert Seluruh Folder")
        print(W + "  [0]  Exit")
        print(G + "\n  ================================================================" + RESET)

        choice = input(G + "\n  [?] Choose: " + RESET).strip()

        if choice == "1":
            convert_single()
            input("\n  Tekan Enter untuk kembali...")
        elif choice == "2":
            convert_folder()
            input("\n  Tekan Enter untuk kembali...")
        elif choice == "0":
            clear()
            print(G + "\n  Thanks for using SKYVEE TECH - Image Converter\n" + RESET)
            time.sleep(3)
            sys.exit(0)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(R + "\n\n  [!] Interrupted." + RESET)
        sys.exit(0)
