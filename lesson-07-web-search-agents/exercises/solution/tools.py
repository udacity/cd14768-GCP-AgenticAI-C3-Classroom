def calculate_percentage_change(initial_value: float, final_value: float):
    """Calculates the percentage change between two numbers."""
    if initial_value == 0:
        return {"error": "Initial value cannot be zero."}
    percentage_change = ((final_value - initial_value) / initial_value) * 100
    return {"percentage_change": percentage_change}

def calculate_profit_or_loss(number_of_shares: int, purchase_price: float, current_price: float):
    """Calculates the profit or loss from a stock transaction."""
    total_cost = number_of_shares * purchase_price
    current_value = number_of_shares * current_price
    profit_or_loss = current_value - total_cost
    return {"profit_or_loss": profit_or_loss}
