import os
import sys
import io
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

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def header():
    clear()
    print(G + """
  ================================================================
  
         SKYVEE TECH - IMAGE COMPRESSOR v1.0
  
  ================================================================
    """ + RESET)

def format_size(b):
    if b < 1024:
        return f"{b} B"
    elif b < 1024 * 1024:
        return f"{b/1024:.1f} KB"
    else:
        return f"{b/(1024*1024):.2f} MB"

def parse_target_size(text):
    text = text.strip().lower()
    try:
        if text.endswith('mb'):
            return int(float(text[:-2]) * 1024 * 1024)
        elif text.endswith('kb'):
            return int(float(text[:-2]) * 1024)
        else:
            return int(text)
    except:
        return None

def compress_to_target(img, target_bytes):
    lo, hi = 1, 95
    best_buf = None
    best_quality = 50

    while lo <= hi:
        mid = (lo + hi) // 2
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=mid, optimize=True)
        size = buf.tell()

        if size <= target_bytes:
            best_buf = buf
            best_quality = mid
            lo = mid + 1
        else:
            hi = mid - 1

    return best_buf, best_quality

def compress_image(img_path, mode, quality=None, target_bytes=None, output_folder=None):
    img_path = Path(img_path)
    size_before = img_path.stat().st_size

    img = Image.open(img_path)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    os.makedirs(output_folder, exist_ok=True)
    out_path = Path(output_folder) / (img_path.stem + '.jpg')

    if mode == 'quality':
        img.save(out_path, 'JPEG', quality=quality, optimize=True)
    elif mode == 'target':
        buf, used_quality = compress_to_target(img, target_bytes)
        if buf is None:
            return None, None, None
        buf.seek(0)
        with open(out_path, 'wb') as f:
            f.write(buf.read())

    size_after = os.path.getsize(out_path)
    saved = size_before - size_after
    saved_pct = (saved / size_before * 100) if size_before > 0 else 0
    return size_before, size_after, saved_pct

def pick_mode():
    print(W + "\n  Pilih mode kompresi:")
    print(W + "  [1]  Berdasarkan Kualitas (High/Medium/Low/Custom %)")
    print(W + "  [2]  Berdasarkan Target Ukuran (contoh: 500kb, 1mb)")
    return input(G + "\n  [?] Choose: " + RESET).strip()

def pick_quality():
    print(W + "\n  Pilih kualitas:")
    print(W + "  [1]  High   (85%)")
    print(W + "  [2]  Medium (65%)")
    print(W + "  [3]  Low    (40%)")
    print(W + "  [4]  Custom (1-95)")
    choice = input(G + "\n  [?] Choose: " + RESET).strip()
    if choice == "1": return 85
    elif choice == "2": return 65
    elif choice == "3": return 40
    elif choice == "4":
        try:
            q = int(input(C + "  [?] Quality (1-95): " + RESET).strip())
            return max(1, min(95, q))
        except:
            return 75
    else:
        return 75

def pick_target():
    print(W + "\n  Masukkan target ukuran file:")
    print(W + "  Contoh: 500kb, 1mb, 200kb")
    raw = input(C + "  [?] Target size: " + RESET).strip()
    target = parse_target_size(raw)
    if not target:
        print(R + "  [-] Format tidak valid! Gunakan contoh: 500kb / 1mb" + RESET)
    return target

def do_single(filepath):
    header()
    filepath = filepath.strip().strip('"')

    supported = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff']
    if not Path(filepath).exists():
        print(R + "  [-] File tidak ditemukan!" + RESET)
        return
    if Path(filepath).suffix.lower() not in supported:
        print(R + "  [-] Format tidak didukung!" + RESET)
        return

    output_folder = str(Path(filepath).parent / "compressed")
    mode_choice = pick_mode()

    if mode_choice == "1":
        quality = pick_quality()
        size_before, size_after, saved_pct = compress_image(filepath, 'quality', quality=quality, output_folder=output_folder)
    elif mode_choice == "2":
        target = pick_target()
        if not target:
            return
        print(Y + "\n  [*] Mencari kualitas terbaik..." + RESET)
        size_before, size_after, saved_pct = compress_image(filepath, 'target', target_bytes=target, output_folder=output_folder)
    else:
        return

    if size_before is None:
        print(R + "  [-] Gagal mengompresi, target terlalu kecil." + RESET)
        return

    print(G + f"\n  [+] Selesai!" + RESET)
    print(W + f"  File          : {Path(filepath).name}")
    print(W + f"  Size sebelum  : {format_size(size_before)}")
    print(W + f"  Size sesudah  : {format_size(size_after)}")
    print(G + f"  Hemat         : {saved_pct:.1f}%" + RESET)
    print(G + f"  Output        : {output_folder}" + RESET)

def do_folder(folderpath):
    header()
    folderpath = folderpath.strip().strip('"')

    supported = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff']
    files = [f for f in Path(folderpath).iterdir() if f.suffix.lower() in supported]

    if not files:
        print(Y + "  [!] Tidak ada foto yang didukung di folder ini." + RESET)
        return

    output_folder = str(Path(folderpath) / "compressed")
    mode_choice = pick_mode()
    quality = None
    target = None

    if mode_choice == "1":
        quality = pick_quality()
    elif mode_choice == "2":
        target = pick_target()
        if not target:
            return
        print(Y + "\n  [*] Mencari kualitas terbaik untuk setiap foto..." + RESET)
    else:
        return

    total_before = 0
    total_after = 0
    success = 0
    failed = 0

    print(G + f"\n  [*] Ditemukan {len(files)} foto. Memproses...\n" + RESET)
    print(G + f"  {'No':<4} {'Filename':<35} {'Before':<12} {'After':<12} {'Saved'}" + RESET)
    print(G + "  " + "─"*65 + RESET)

    for i, fp in enumerate(files, 1):
        try:
            if mode_choice == "1":
                sb, sa, spct = compress_image(fp, 'quality', quality=quality, output_folder=output_folder)
            else:
                sb, sa, spct = compress_image(fp, 'target', target_bytes=target, output_folder=output_folder)

            if sb is None:
                raise Exception("Target terlalu kecil")

            total_before += sb
            total_after += sa
            color = G if sa < sb else Y
            print(color + f"  {i:<4} {fp.name:<35} {format_size(sb):<12} {format_size(sa):<12} -{spct:.1f}%" + RESET)
            success += 1
        except Exception as e:
            print(R + f"  {i:<4} {fp.name:<35} ERROR: {str(e)[:30]}" + RESET)
            failed += 1

    total_saved = total_before - total_after
    total_pct = (total_saved / total_before * 100) if total_before > 0 else 0

    print(G + "\n  " + "─"*65 + RESET)
    print(G + f"\n  [+] Selesai!" + RESET)
    print(W + f"  Total foto    : {len(files)}")
    print(W + f"  Berhasil      : {success}")
    print(W + f"  Gagal         : {failed}")
    print(W + f"  Size sebelum  : {format_size(total_before)}")
    print(W + f"  Size sesudah  : {format_size(total_after)}")
    print(G + f"  Total hemat   : {format_size(total_saved)} ({total_pct:.1f}%)" + RESET)
    print(G + f"  Output        : {output_folder}" + RESET)

def menu():
    while True:
        header()
        print(W + "  [1]  Compress 1 Foto")
        print(W + "  [2]  Compress Seluruh Folder")
        print(W + "  [0]  Exit")
        print(G + "\n  ================================================================" + RESET)

        choice = input(G + "\n  [?] Choose: " + RESET).strip()

        if choice == "1":
            header()
            filepath = input(C + "  [?] Path foto   : " + RESET)
            do_single(filepath)
            input("\n  Tekan Enter untuk kembali...")

        elif choice == "2":
            header()
            folder = input(C + "  [?] Path folder : " + RESET)
            do_folder(folder)
            input("\n  Tekan Enter untuk kembali...")

        elif choice == "0":
            clear()
            print(G + "\n  Thanks for using SKYVEE TECH - Bulk Image Compressor\n" + RESET)
            sys.exit(0)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(R + "\n\n  [!] Interrupted." + RESET)
        sys.exit(0)
