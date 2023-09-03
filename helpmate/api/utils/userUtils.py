import re

# Function to validate login input
def validate_login_input(data):
    errors = {}

    # Convert empty fields to an empty string so we can use validation functions
    data['email'] = data.get('email', '')
    data['password'] = data.get('password', '')

    # Email checks
    if not data['email']:
        errors['email'] = 'Email field is required'
    elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
        errors['email'] = 'Email is invalid'

    # Password checks
    if not data['password']:
        errors['password'] = 'Password field is required'

    return {
        'errors': errors,
        'is_valid': not bool(errors)
    }

# Function to validate registration input
def validate_register_input(data):
    errors = {}
    
    # Convert empty fields to an empty string so we can use validator functions
    data['name'] = data.get('name', '').strip()
    data['email'] = data.get('email', '').strip()
    data['password'] = data.get('password', '').strip()
    data['password2'] = data.get('password2', '').strip()
    
    # Name checks
    if not data['name']:
        errors['name'] = "Name field is required"

    # Email checks
    if not data['email']:
        errors['email'] = "Email field is required"
    elif not re.match(r'^\S+@\S+\.\S+$', data['email']):
        errors['email'] = "Email is invalid"

    # Password checks
    if not data['password']:
        errors['password'] = "Password field is required"
    if not data['password2']:
        errors['password2'] = "Confirm password field is required"
    if len(data['password']) < 6 or len(data['password']) > 30:
        errors['password'] = "Password must be between 6 and 30 characters"
    if data['password'] != data['password2']:
        errors['password2'] = "Passwords must match"

    return {
        'errors': errors,
        'is_valid': not bool(errors)
    }
