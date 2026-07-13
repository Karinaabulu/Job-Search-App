def verify_nin(nin: str):
    # TEMPORARY: fake response until we plug in the real NIN provider API
    # Later this will call Prembly/VerifyMe with the actual NIN
    if len(nin) != 11 or not nin.isdigit():
        return None

    return {
        "full_name": "Test User",
        "date_of_birth": "2000-01-01"
    }