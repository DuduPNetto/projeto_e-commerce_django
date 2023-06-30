def cart_total_qtt(cart):
    return sum([item['quantity'] for item in cart.values()])


def cart_totals(cart):
    return sum(
        [
            item.get('promotional_unitary_price')
            if item.get('promotional_unitary_price')
            else item.get('unitary_price')
            for item in cart.values()
        ]
    )
