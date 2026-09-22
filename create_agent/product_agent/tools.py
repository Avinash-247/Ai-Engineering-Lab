import json
from langchain_core.tools import tool

@tool
def get_all_products() -> str:
    """
    Get all products from the LReal product catalog.

    Returns:
        str: A pipe-delimited list containing all products.
        Each product is represented on a single line with the following
        attributes:

        product_id | category | product_name | description | price_inr |
        size | how_to_use | benefits | problems_it_solves | suitable_for

    The returned format is designed to be easy for an AI agent to read
    and use when searching or recommending products.

    Example:
        LREAL-SKIN-001 | skin_care | HydraGlow Gentle Face Cleanser |
        A gentle, hydrating facial cleanser... | 349 | 100 ml |
        Wet your face...; Apply a small amount... |
        Cleanses the skin; Helps maintain skin hydration |
        Daily facial dirt; Excess oil |
        Normal skin; Dry skin; Combination skin
    """

    with open("data/products.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    products = data["products"]

    result = [
        "product_id | category | product_name | description | price_inr | "
        "size | how_to_use | benefits | problems_it_solves | suitable_for"
    ]

    for product in products:
        how_to_use = "; ".join(product["how_to_use"])
        benefits = "; ".join(product["benefits"])
        problems_it_solves = "; ".join(product["problems_it_solves"])
        suitable_for = "; ".join(product["suitable_for"])

        result.append(
            f"{product['product_id']} | "
            f"{product['category']} | "
            f"{product['product_name']} | "
            f"{product['description']} | "
            f"{product['price_inr']} | "
            f"{product['size']} | "
            f"{how_to_use} | "
            f"{benefits} | "
            f"{problems_it_solves} | "
            f"{suitable_for}"
        )

    return "\n".join(result)

@tool
def get_product(product_id: str) -> str:
    """
    Get a specific product from the LReal product catalog using its product ID.

    Args:
        product_id (str): Unique product ID of the product to retrieve.
            Example: "LREAL-SKIN-001"

    Returns:
        str: The product details in a single pipe-delimited line containing
        all product attributes:

        product_id | category | product_name | description | price_inr |
        size | how_to_use | benefits | problems_it_solves | suitable_for

        Returns an error message if the specified product ID does not exist.

    Example:
        >>> get_product("LREAL-SKIN-001")
        "LREAL-SKIN-001 | skin_care | HydraGlow Gentle Face Cleanser | ..."

    """
    with open("data/products.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for product in data["products"]:
        if product["product_id"] == product_id:
            how_to_use = "; ".join(product["how_to_use"])
            benefits = "; ".join(product["benefits"])
            problems_it_solves = "; ".join(product["problems_it_solves"])
            suitable_for = "; ".join(product["suitable_for"])

            return (
                f"{product['product_id']} | "
                f"{product['category']} | "
                f"{product['product_name']} | "
                f"{product['description']} | "
                f"{product['price_inr']} | "
                f"{product['size']} | "
                f"{how_to_use} | "
                f"{benefits} | "
                f"{problems_it_solves} | "
                f"{suitable_for}"
            )

    return f"Product with product_id '{product_id}' was not found."
