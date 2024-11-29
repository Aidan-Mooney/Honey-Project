def format_api_url(base_url: str, limit: int = 50, **kwargs):
    if not isinstance(base_url, str):
        raise TypeError("base_url must be a string")
    if not isinstance(limit, int):
        raise TypeError("limit must be an int")
    if not 0 < limit <= 1000:
        raise ValueError(
            "limit must be a positive, non-zero integer less than one thousand"
        )
    queries = [f"?limit={limit}"]
    queries += [f"{key}={value}" for key, value in kwargs.items()]
    return base_url + "&".join(queries)
