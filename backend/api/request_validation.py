def validate_request_fields(required_fields=[],
                            optional_fields=[],
                            request_fields={}):
    """DO NOT MANIPULATE request_fields!"""

    keys = list(request_fields.keys())

    try:
        for key in required_fields:
            keys.remove(key)
    except ValueError:
        # Invalid since it did not have some required field
        print("Failed validation due to missing required field")
        return False

    # Pop all optional fields and ensure no leftover trash is left in
    # request_fields
    for key in optional_fields:
        try:
            keys.remove(key, None)  # Ignore exception this time, we only want
                                    # to clear it
        except ValueError:
            pass

    return len(keys) == 0
