"""Kumpe3D Print Commands"""

import os
from pyhtml2pdf import converter
import scan_list_builder as slb
from params import Params as params


def generate_pdf(url, pdf_path, label_type: str, qty: int, enable_print: bool = True):
    """Generate PDF from URL"""
    print(url)
    paper_size = {"height": 1.97, "width": 3.15}
    if label_type == "product_label":
        pass
    elif label_type == "barcode_label":
        paper_size["height"] = 1.18
        paper_size["width"] = 1.57
    elif label_type == "wide_barcode_label":
        paper_size["height"] = 1.18
        paper_size["width"] = 1.96
    elif label_type == "square_product_label":
        paper_size["height"] = 1.96
        paper_size["width"] = 1.96
    else:
        raise ValueError(
            f"Generating Label Type {label_type} is not supported. Paper Size is unknown"
        )

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
    print_label(label_type, qty, enable_print)


# Run the function
def generate_label(
    sku: str,
    qr_data: str,
    label_type: str,
    qty: int,
    customer_id=0,
    enable_print: bool = True,
):
    """Generate PDF Product Label"""
    if label_type == "product_label":
        generate_pdf(
            f"{params.WEB.base_url}/product_labels.php?sku="
            + sku
            + "&qr_data="
            + qr_data
            + "&distributor="
            + str(customer_id),
            "product_label.pdf",
            label_type,
            qty,
            enable_print,
        )
    elif label_type == "square_product_label":
        generate_pdf(
            f"{params.WEB.base_url}/product_label_2.php?sku="
            + sku
            + "&qr_data="
            + qr_data
            + "&distributor="
            + str(customer_id),
            "square_product_label.pdf",
            label_type,
            qty,
            enable_print,
        )
    elif label_type == "barcode_label":
        generate_pdf(
            f"{params.WEB.base_url}/barcode_label.php?sku="
            + sku
            + "&distributor="
            + str(customer_id),
            "barcode_label.pdf",
            label_type,
            qty,
            enable_print,
        )
    elif label_type == "wide_barcode_label":
        generate_pdf(
            f"{params.WEB.base_url}/wide_barcode_label.php?sku="
            + sku
            + "&distributor="
            + str(customer_id),
            "wide_barcode_label.pdf",
            label_type,
            qty,
            enable_print,
        )
    else:
        raise ValueError(
            f"Generating Label Type {label_type} Not Supported. URL is unknown."
        )


def print_label(label_type: str, qty: int, enable_print: bool = True):
    """Print Product Label PDF to Printer"""

    if enable_print:
        if label_type == "product_label":
            os.system(
                f"lp -d Product_Label_Printer -o media=50x80mm -o orientation-requested=4 product_label.pdf -n {qty}"  # pylint: disable=line-too-long
            )
        elif label_type == "square_product_label":
            os.system(
                f"lp -d Square_Product_Label_Printer -o media=50x50mm square_product_label.pdf -n {qty}"  # pylint: disable=line-too-long
            )
        elif label_type == "barcode_label":
            os.system(
                f"lp -d Barcode_Label_Printer -o media=40x30mm barcode_label.pdf -n {qty}"
            )
        elif label_type == "wide_barcode_label":
            os.system(
                f"lp -d Wide_Barcode_Label_Printer -o media=50x30mm wide_barcode_label.pdf -n {qty}"
            )
        else:
            raise ValueError(
                f"Printing Label Type {label_type} Not Supported. Printer name is unknown."
            )
    else:
        pass


def print_product_label(
    sku: str,
    qr_data: str,
    label_type: str,
    qty: int = 1,
    customer_id=0,
    enable_print: bool = True,
):
    """Prints Product Label"""
    try:
        print(sku)
        generate_label(sku, qr_data, label_type, qty, customer_id, enable_print)
    except KeyError:
        print(f"Invalid SKU {sku}")


def print_label_bundle(
    sku: str, qty: int = 1, customer_id=0, enable_print: bool = True
):
    """Print Product Label and Barcode Bundle"""
    scanned_list = slb.build_k3d_item_dict(sku)
    sku1_data = scanned_list[0]
    sku1 = sku1_data["sku"]
    print_product_label(sku1, sku, "product_label", 1, customer_id, enable_print)
    print_product_label(
        sku1, sku, "square_product_label", qty, customer_id, enable_print
    )
    print_product_label(sku1, sku, "barcode_label", qty, customer_id, enable_print)
