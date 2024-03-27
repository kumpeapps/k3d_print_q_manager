"""Kumpe3D Print Q Manager"""

from flask import Flask
import printcommands


app = Flask(__name__)


@app.route("/print_label/<int:customer_id>/<string:sku>/<str:label>/<int:qty>", methods=["POST"])
def print_label(customer_id, sku, label, qty):
    """Print Label"""
    printcommands.print_product_label(sku, label, qty, customer_id)


@app.route("/print_bundle/<int:customer_id>/<string:sku>/<int:qty>", methods=["POST"])
def print_bundle(customer_id, sku, qty):
    """Print Label Bundle"""
    printcommands.print_label_bundle(sku, qty, customer_id)


if __name__ == "__main__":
    app.run(port="8081")
