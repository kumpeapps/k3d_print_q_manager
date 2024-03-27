"""Kumpe3D Print Q Manager"""

from flask import Flask, request
import printcommands


app = Flask(__name__)


@app.route("/print_label/<int:customer_id>/<string:sku>/<string:label>/<int:qty>", methods=["POST"])
def print_label(customer_id, sku, label, qty):
    """Print Label"""
    print(f"Customer ID: {customer_id}")
    print(f"sku: {sku}")
    print(f"Label: {label}")
    print(f"qty: {qty}")
    try:
        printcommands.print_product_label(sku, label, qty, customer_id)
        return "OK"
    except ValueError:
        return f"Label Type {label} not supported", 422

@app.route("/print_bundle/<int:customer_id>/<string:sku>/<int:qty>", methods=["POST"])
def print_bundle(customer_id, sku, qty):
    """Print Label Bundle"""
    try:
        printcommands.print_label_bundle(sku, qty, customer_id)
        return "OK"
    except:
        return "Unknown Error", 422


if __name__ == "__main__":
    app.run(port="8081")
