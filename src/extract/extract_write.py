from src.extract.write_args import write_args


def extract_write(base_path: str, purchases: dict):
    lines_saved = 0
    for purchase in purchases:
        purchaseID = purchase["purchaseUUID1"]
        try:
            latitude = purchase["gpsCoordinates"]["latitude"]
            longitude = purchase["gpsCoordinates"]["longitude"]
        except KeyError:
            latitude = ""
            longitude = ""
        write_args(
            f"{base_path}/purchases.csv",
            purchaseID,
            purchase["amount"],
            purchase["created"],
            latitude,
            longitude,
        )
        lines_saved += 1
        for product in purchase["products"]:
            name = product.get("name", None)
            if name is None:
                continue
            write_args(
                f"{base_path}/products.csv",
                name,
                product["quantity"],
                purchaseID,
            )
            lines_saved += 1
        for payment in purchase["payments"]:
            if payment["type"] == "IZETTLE_CARD":
                write_args(
                    f"{base_path}/card.csv",
                    payment["uuid"],
                    payment["attributes"]["maskedPan"],
                    payment["amount"],
                    purchaseID,
                )
                lines_saved += 1
            if payment["type"] == "IZETTLE_CASH":
                write_args(
                    f"{base_path}/cash.csv",
                    payment["uuid"],
                    payment["amount"],
                    purchaseID,
                )
                lines_saved += 1
    return lines_saved
