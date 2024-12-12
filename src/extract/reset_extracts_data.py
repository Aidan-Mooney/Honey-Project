def reset_extracts_data():
    base_url = "data/extract"
    table_data = {
        "card.csv": "uuid,referenceNumber,amount,purchaseUUID1",
        "cash.csv": "uuid,amount,purchaseUUID1",
        "products.csv": "productUuid,name,quantity,purchaseUUID1",
        "purchases.csv": "purchaseUUID1,amount,created,latitude,longitude",
    }
    for file_name, headings in table_data.items():
        with open(f"{base_url}/{file_name}", "w", encoding="utf-8") as f:
            f.write(headings + "\n")
