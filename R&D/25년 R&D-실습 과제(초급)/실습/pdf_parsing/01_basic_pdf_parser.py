"""
[*] PDF [*] [*] [*] (PyPDF2 [*])

[*] [*] PyPDF2 [*] [*] PDF [*] [*] [*] [*] [*].

[*] [*]:
1. PDF [*] [*] [*] [*] [*]
2. [*] [*] [*] [*]
3. PDF [*] [*] ([*], [*], [*])
4. [*] [*] [*] [*]

[*] [*]:
    pip install PyPDF2
"""

import os

# PyPDF2 [*] 3.x[*] pypdf[*] import
try:
    from pypdf import PdfReader, PdfWriter, PdfMerger
    PYPDF_VERSION = "3.x"
except ImportError:
    try:
        from PyPDF2 import PdfReader, PdfWriter, PdfMerger
        PYPDF_VERSION = "2.x"
    except ImportError:
        print("[ERROR] PyPDF2[*] [*] [*].")
        print("[*] [*]: pip install PyPDF2")
        exit(1)


def get_pdf_info(pdf_path):
    """
    PDF [*] [*] [*] [*]

    Args:
        pdf_path (str): PDF [*] [*]

    Returns:
        dict: PDF [*] [*]

    [*] [*]:
        - [*] [*]
        - [*] ([*], [*], [*] [*])
        - [*] [*]
        - PDF [*]
    """
    try:
        # PDF [*] [*] [*] [*]('rb')[*] [*]
        with open(pdf_path, 'rb') as file:
            # PdfReader [*] [*]
            reader = PdfReader(file)

            # [*] [*] [*]
            info = {
                'file_path': pdf_path,
                'num_pages': len(reader.pages),  # [*] [*] [*]
                'is_encrypted': reader.is_encrypted,  # [*] [*]
            }

            # [*] [*] ([*] [*] [*])
            metadata = reader.metadata
            if metadata:
                info['metadata'] = {
                    'title': metadata.get('/Title', 'N/A'),
                    'author': metadata.get('/Author', 'N/A'),
                    'subject': metadata.get('/Subject', 'N/A'),
                    'creator': metadata.get('/Creator', 'N/A'),
                    'producer': metadata.get('/Producer', 'N/A'),
                    'creation_date': metadata.get('/CreationDate', 'N/A'),
                    'modification_date': metadata.get('/ModDate', 'N/A'),
                }
            else:
                info['metadata'] = None

            # [*] [*]
            print("=" * 60)
            print("[FILE] PDF [*] [*]")
            print("=" * 60)
            print(f"[*]: {pdf_path}")
            print(f"[*] [*]: {info['num_pages']}")
            print(f"[*]: {'[*]' if info['is_encrypted'] else '[*]'}")

            if info['metadata']:
                print("\n[LIST] [*]:")
                for key, value in info['metadata'].items():
                    print(f"  {key}: {value}")

            return info

    except FileNotFoundError:
        print(f"[ERROR] [*] [*] [*] [*]: {pdf_path}")
        return None
    except Exception as e:
        print(f"[ERROR] [*] [*]: {e}")
        return None


def extract_text_from_page(pdf_path, page_number):
    """
    [*] [*] [*] [*]

    Args:
        pdf_path (str): PDF [*] [*]
        page_number (int): [*] [*] (1[*] [*])

    Returns:
        str: [*] [*]

    [*]:
        - PyPDF2[*] [*] [*] PDF[*] [*] [*] [*]
        - [*] [*] [*] [*] [*] [*] [*]
        - [*] [*] [*] [*] [*] [*] [*] [*]
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)

            # [*] [*] [*] (1-based → 0-based)
            if page_number < 1 or page_number > len(reader.pages):
                print(f"[ERROR] [*] [*] [*]: {page_number}")
                print(f"   ([*] [*]: 1 ~ {len(reader.pages)})")
                return None

            # [*] [*] [*] (0-based [*])
            page = reader.pages[page_number - 1]

            # [*] [*]
            text = page.extract_text()

            # [*] [*]
            print(f"\n[FILE] [*] {page_number} [*] [*]")
            print("=" * 60)
            print(text)
            print("=" * 60)
            print(f"[*] [*] [*]: {len(text)}[*]\n")

            return text

    except Exception as e:
        print(f"[ERROR] [*] [*] [*]: {e}")
        return None


def extract_all_text(pdf_path, save_to_file=None):
    """
    PDF [*] [*] [*] [*]

    Args:
        pdf_path (str): PDF [*] [*]
        save_to_file (str, optional): [*] [*] [*] [*]

    Returns:
        str: [*] [*]

    [*]:
        - [*] [*] [*]
        - [*] [*] [*] [*]
        - [*] [*]
    """
    try:
        full_text = []

        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)

            print(f"\n[BOOKS] [*] [*] [*] [*] ([*] {total_pages}[*])")

            # [*] [*] [*]
            for page_num in range(total_pages):
                page = reader.pages[page_num]
                text = page.extract_text()

                # [*] [*] [*] [*] [*]
                full_text.append(f"=== [*] {page_num + 1} ===\n{text}\n")

                # [*] [*] [*]
                if (page_num + 1) % 10 == 0 or (page_num + 1) == total_pages:
                    print(f"  [*]: {page_num + 1}/{total_pages} [*]")

            # [*] [*] [*]
            combined_text = '\n'.join(full_text)

            print(f"[OK] [*] [*]: [*] {len(combined_text)}[*]")

            # [*] [*] ([*])
            if save_to_file:
                with open(save_to_file, 'w', encoding='utf-8') as f:
                    f.write(combined_text)
                print(f"[SAVE] [*] [*] [*]: {save_to_file}")

            return combined_text

    except Exception as e:
        print(f"[ERROR] [*] [*] [*] [*]: {e}")
        return None


def merge_pdfs(pdf_list, output_path):
    """
    [*] PDF [*] [*] [*]

    Args:
        pdf_list (list): [*] PDF [*] [*] [*]
        output_path (str): [*] PDF [*] [*]

    [*] [*]:
        merge_pdfs(['doc1.pdf', 'doc2.pdf', 'doc3.pdf'], 'merged.pdf')

    [*]:
        - [*] [*] [*] [*]
        - [*] [*] [*] [*]
    """
    try:
        # PdfMerger [*] [*]
        merger = PdfMerger()

        print(f"\n[DOC] PDF [*] [*] ({len(pdf_list)}[*] [*])")

        # [*] PDF [*] [*] [*]
        for i, pdf_file in enumerate(pdf_list, 1):
            if not os.path.exists(pdf_file):
                print(f"[WARN]  [*] [*] [*] [*]: {pdf_file}")
                continue

            merger.append(pdf_file)
            print(f"  {i}. {pdf_file} [*]")

        # [*] PDF [*]
        merger.write(output_path)
        merger.close()

        print(f"[OK] [*] [*]: {output_path}")

    except Exception as e:
        print(f"[ERROR] PDF [*] [*]: {e}")


def split_pdf(pdf_path, output_dir):
    """
    PDF[*] [*] [*]

    Args:
        pdf_path (str): [*] PDF [*]
        output_dir (str): [*] [*] [*] [*]

    [*]:
        - page_1.pdf, page_2.pdf, ... [*] [*]

    [*]:
        - [*] [*] [*]
        - [*] PDF[*] [*] [*] [*]
    """
    try:
        # [*] [*] [*]
        os.makedirs(output_dir, exist_ok=True)

        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)

            print(f"\n[CUT]  PDF [*] [*] ([*] {total_pages}[*])")

            # [*] [*] [*] [*] [*]
            for page_num, page in enumerate(reader.pages, start=1):
                # [*] PdfWriter [*] [*]
                writer = PdfWriter()

                # [*] [*] [*]
                writer.add_page(page)

                # [*] [*]
                output_file = os.path.join(output_dir, f"page_{page_num}.pdf")

                # PDF [*] [*]
                with open(output_file, 'wb') as output:
                    writer.write(output)

                print(f"  [*] {page_num} [*]: {output_file}")

            print(f"[OK] [*] [*]: {output_dir}/")

    except Exception as e:
        print(f"[ERROR] PDF [*] [*]: {e}")


def rotate_pages(pdf_path, output_path, rotation=90):
    """
    PDF [*] [*]

    Args:
        pdf_path (str): [*] PDF [*]
        output_path (str): [*] PDF [*] [*]
        rotation (int): [*] [*] (90, 180, 270)

    [*]:
        - [*] [*] [*]
        - 90[*] [*] [*] [*]
    """
    try:
        valid_rotations = [90, 180, 270]
        if rotation not in valid_rotations:
            print(f"[ERROR] [*] [*] [*] [*]: {rotation}")
            print(f"   ([*] [*]: {valid_rotations})")
            return

        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            writer = PdfWriter()

            print(f"\n[ROTATE] PDF [*] [*] ({rotation}[*])")

            # [*] [*] [*]
            for page_num, page in enumerate(reader.pages, start=1):
                # [*] [*] ([*] [*])
                page.rotate(rotation)
                writer.add_page(page)

                print(f"  [*] {page_num} [*]")

            # [*] PDF [*]
            with open(output_path, 'wb') as output:
                writer.write(output)

            print(f"[OK] [*] [*]: {output_path}")

    except Exception as e:
        print(f"[ERROR] PDF [*] [*]: {e}")


def add_metadata(input_pdf, output_pdf, metadata_dict):
    """
    PDF[*] [*] [*]/[*]

    Args:
        input_pdf (str): [*] PDF
        output_pdf (str): [*] PDF
        metadata_dict (dict): [*] [*]

    [*] [*]:
        {
            '/Title': '[*] [*]',
            '/Author': '[*] [*]',
            '/Subject': '[*] [*]',
            '/Keywords': '[*]1, [*]2'
        }
    """
    try:
        with open(input_pdf, 'rb') as file:
            reader = PdfReader(file)
            writer = PdfWriter()

            # [*] [*] [*]
            for page in reader.pages:
                writer.add_page(page)

            # [*] [*]
            writer.add_metadata(metadata_dict)

            # [*]
            with open(output_pdf, 'wb') as output:
                writer.write(output)

            print(f"[OK] [*] [*] [*]: {output_pdf}")

            # [*] [*] [*]
            print("\n[LIST] [*] [*]:")
            for key, value in metadata_dict.items():
                print(f"  {key}: {value}")

    except Exception as e:
        print(f"[ERROR] [*] [*] [*]: {e}")


def main():
    """
    [*] [*]: [*] [*] [*]
    """
    print("=" * 60)
    print(f"PDF [*] [*] [*] (PyPDF2 {PYPDF_VERSION})")
    print("=" * 60)

    # [*] PDF [*] [*] - RDA.pdf [*] [*]
    sample_pdf = "../data/RDA.pdf"

    if not os.path.exists(sample_pdf):
        print(f"\n[ERROR] PDF [*] [*] [*] [*]: {sample_pdf}")
        print("RDA.pdf [*] [*] [*] [*].")
        return

    # 1. PDF [*] [*]
    print("\n" + "=" * 60)
    print("1. PDF [*] [*]")
    print("=" * 60)
    info = get_pdf_info(sample_pdf)

    if info and info['num_pages'] > 0:
        # 2. [*] [*] [*] [*]
        print("\n" + "=" * 60)
        print("2. [*] [*] [*] [*]")
        print("=" * 60)
        extract_text_from_page(sample_pdf, 1)

        # 3. [*] [*] [*]
        print("\n" + "=" * 60)
        print("3. [*] [*] [*]")
        print("=" * 60)
        extract_all_text(sample_pdf, save_to_file="data/rda_extracted_text.txt")

    # 4. PDF [*] ([*])
    print("\n" + "=" * 60)
    print("4. PDF [*] [*]")
    print("=" * 60)
    split_pdf(sample_pdf, "data/rda_split_pages")

    # 5. [*] [*]
    print("\n" + "=" * 60)
    print("5. [*] [*]")
    print("=" * 60)
    new_metadata = {
        '/Title': 'RDA Document Analysis',
        '/Author': 'R&D Team',
        '/Subject': 'PDF [*] [*] [*]',
        '/Keywords': 'Python, PDF, PyPDF2, RDA'
    }
    add_metadata(sample_pdf, "data/rda_with_metadata.pdf", new_metadata)

    print("\n" + "=" * 60)
    print("[*] [*]!")
    print("=" * 60)

    print("\n[TIP] [*] [*] [*]:")
    print("  1. [*] PDF[*] [*] [*] [*]")
    print("  2. PDF [*] [*] [*] [*]")
    print("  3. [*] [*] [*]")
    print("  4. [*] PDF [*]")


if __name__ == "__main__":
    main()
