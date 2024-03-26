"""Kumpe3D Print Commands"""

import os
from pyhtml2pdf import converter


def generate_pdf(url, pdf_path, label_type: str, qty: int):
    """Generate PDF from URL"""
    print(url)
    paper_size = {"height": 1.97, "width": 3.15}
    if label_type == "product label":
        pass
    elif label_type == "barcode label":
        paper_size["height"] = 1.18
        paper_size["width"] = 1.57
    elif label_type == "square product label":
        paper_size["height"] = 1.96
        paper_size["width"] = 1.96
    else:
        raise ValueError(f"Label Type {label_type} is not supported")

    converter.convert(
        url,
        pdf_path,
        print_options={
            "marginBotton": 0,
            "marginTop": 0,
            "marginLeft": 0,
            "marginRight": 0,
            "paperHeight": paper_size["height"],
            "paperWidth": paper_size["width"],
        },
    )
    print_label(label_type, qty)


# Run the function
def generate_label(sku: str, label_type: str, qty: int, customer_id=0):
    """Generate PDF Product Label"""
    if label_type == "product label":
        generate_pdf(
            "https://www.kumpe3d.com/product_labels.php?sku="
            + sku
            + "&customer_id="
            + customer_id,
            "product_label.pdf",
            label_type,
            qty,
        )
    elif label_type == "square product label":
        generate_pdf(
            "https://www.kumpe3d.com/product_label_2.php?sku="
            + sku
            + "&customer_id="
            + customer_id,
            "square_product_label.pdf",
            label_type,
            qty,
        )
    elif label_type == "barcode label":
        generate_pdf(
            "https://www.kumpe3d.com/barcode_label.php?sku="
            + sku
            + "&customer_id="
            + customer_id,
            "barcode_label.pdf",
            label_type,
            qty,
        )
    else:
        raise ValueError(f"Label Type {label_type} Not Supported")


def print_label(label_type: str, qty: int):
    """Print Product Label PDF to Printer"""
    # Only print in production environment
    enable_print = True
    if enable_print:
        if label_type == "product label":
            os.system(
                f"lp -d Product_Label_Printer -o media=50x80mm -o orientation-requested=4 product_label.pdf -n {qty}" #pylint: disable=line-too-long
            )
        elif label_type == "square product label":
            os.system(
                f"lp -d Square_Product_Label_Printer -o media=50x50mm square_product_label.pdf -n {qty}" #pylint: disable=line-too-long
            )
        elif label_type == "barcode label":
            os.system(
                f"lp -d Barcode_Label_Printer -o media=40x30mm barcode_label.pdf -n {qty}"
            )
    else:
        pass


def print_product_label(sku: str, label_type: str, qty: int = 1, customer_id=0):
    """Prints Product Label"""
    try:
        print(sku)
        generate_label(sku, label_type, qty, customer_id)
    except KeyError:
        print(f"Invalid SKU {sku}")


def print_label_bundle(sku: str, qty: int = 1, customer_id=0):
    """Print Product Label and Barcode Bundle"""
    print_product_label(sku, "product label", 1, customer_id)
    print_product_label(sku, "square product label", qty, customer_id)
    print_product_label(sku, "barcode label", qty, customer_id)
