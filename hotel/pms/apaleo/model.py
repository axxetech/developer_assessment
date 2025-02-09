from hotel.pms.model import UpsellProductAdapter, UpsellProduct


# --- Apaleo Adapter Implementation ---
class ApaleoUpsellProductAdapter(UpsellProductAdapter):
    """
    Adapter for converting Apaleo upsell product data to the unified UpsellProduct model.
    """
    def convert(self) -> UpsellProduct:
        # For Apaleo, we expect a nested 'defaultGrossPrice' dict and an 'ageCategoryId'
        default_price = self.raw_data.get("defaultGrossPrice", {})
        amount = default_price.get("amount", 0)
        currency = default_price.get("currency", "")
        price_str = f"{amount} {currency}"
        return UpsellProduct(
            id=self.raw_data.get("id", ""),
            name=self.raw_data.get("name", ""),
            code=self.raw_data.get("code", ""),
            description=self.raw_data.get("description", ""),
            price=price_str,
            age_category=self.raw_data.get("ageCategoryId", "")
        )