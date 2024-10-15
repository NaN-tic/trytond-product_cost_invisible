# This file is part product_cost_invisible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import product
from . import purchase
from . import lot
from . import stock
from . import stock_valued


def register():
    Pool.register(
        product.Template,
        product.Product,
        module='product_cost_invisible', type_='model')
    Pool.register(
        purchase.Purchase,
        purchase.PurchaseLine,
        purchase.ProductSupplier,
        depends=['purchase'],
        module='product_cost_invisible', type_='model')
    Pool.register(
        stock.Location,
        depends=['stock'],
        module='product_cost_invisible', type_='model')
    Pool.register(
        lot.Lot,
        depends=['stock_lot_cost'],
        module='product_cost_invisible', type_='model')
    Pool.register(
        stock_valued.ShipmentIn,
        stock_valued.ShipmentOut,
        stock_valued.ShipmentOutReturn,
        depends=['stock_valued'],
        module='product_cost_invisible', type_='model')
