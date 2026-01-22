"""
Test script to verify password encryption is working correctly
Run with: python manage.py shell < test_password_encryption.py
"""
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, identify_hasher

print("\n" + "="*60)
print("Password Encryption Test")
print("="*60 + "\n")

# Create a test user
test_username = 'security_test_user'
test_password = 'SecureP@ssw0rd123!'

# Clean up any existing test user
User.objects.filter(username=test_username).delete()

# Create new user
print(f"Creating test user: {test_username}")
user = User.objects.create_user(
    username=test_username,
    email='test@example.com',
    password=test_password
)
print(f"✓ User created successfully\n")

# Check the password hash
print("Password Hash Details:")
print("-" * 60)
print(f"Hash: {user.password[:50]}...")
print(f"Length: {len(user.password)} characters")

# Identify the hasher
try:
    hasher = identify_hasher(user.password)
    algorithm = hasher.algorithm
    print(f"Algorithm: {algorithm}")
    
    if algorithm == 'argon2':
        print("✓ SUCCESS: Using Argon2 (Most Secure)")
    elif algorithm in ['pbkdf2_sha256', 'bcrypt_sha256']:
        print("⚠ WARNING: Using older algorithm, should be Argon2")
    else:
        print("✗ ERROR: Using insecure algorithm")
except Exception as e:
    print(f"✗ ERROR: Could not identify hasher: {e}")

# Verify password checking works
print("\n" + "-" * 60)
print("Password Verification Test:")
print("-" * 60)

# Test correct password
is_correct = check_password(test_password, user.password)
print(f"Correct password: {is_correct}")
if is_correct:
    print("✓ Password verification works correctly")
else:
    print("✗ ERROR: Password verification failed")

# Test wrong password
is_wrong = check_password('WrongPassword', user.password)
print(f"Wrong password rejected: {not is_wrong}")
if not is_wrong:
    print("✓ Wrong passwords are correctly rejected")
else:
    print("✗ ERROR: Wrong password was accepted")

# Clean up
print("\n" + "-" * 60)
print("Cleaning up test user...")
user.delete()
print("✓ Test user deleted")

print("\n" + "="*60)
print("Test Complete!")
print("="*60 + "\n")

print("Summary:")
print("--------")
if algorithm == 'argon2' and is_correct and not is_wrong:
    print("✓✓✓ ALL TESTS PASSED - Password encryption is working perfectly!")
    print("✓ Argon2 algorithm is being used")
    print("✓ Password verification is working")
    print("✓ Security is OPTIMAL")
else:
    print("⚠ Some issues detected. Check the output above.")

print("\nFor more information, run:")
print("  python manage.py check_password_security")
print("")
