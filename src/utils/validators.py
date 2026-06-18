def validate_patient_data(data):
    """
    Validates that all required fields are present and have correct types.
    """
    required_fields = {
        'Maternal Age': int,
        'Education': str,
        'Occupation': str,
        'Location': str,
        'Gravida': int,
        'Parity': int,
        'ANCV': int,
        'PreEC': int,
        'Delivery Mode': str,
        'Complications': str
    }
    
    missing = []
    type_errors = []
    
    for field, field_type in required_fields.items():
        if field not in data:
            missing.append(field)
        else:
            try:
                # Attempt casting for numeric fields
                if field_type == int:
                    int(data[field])
            except (ValueError, TypeError):
                type_errors.append(field)
                
    return {
        "is_valid": len(missing) == 0 and len(type_errors) == 0,
        "missing": missing,
        "type_errors": type_errors
    }
