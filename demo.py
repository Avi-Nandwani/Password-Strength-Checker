from password_strength_checker import PasswordStrengthChecker, rating

DEMO_PASSWORDS = [
    "password",
    "12345678",
    "Abc12345",
    "Qwerty123!",
    "S0lidP@ssword!",
    "Pa$$w0rd2023AA@@"
]

checker = PasswordStrengthChecker()
for pwd in DEMO_PASSWORDS:
    result = checker.evaluate(pwd)
    print(f"\nPassword: {pwd}")
    print(f"Score: {result['score']}/{result['total']}")
    print(f"Rating: {rating(result['score'], result['total'])}")
    if result["score"] == result["total"]:
        print("Excellent!")
    else:
        print("Suggestions:")
        for sug in result["suggestions"]:
            print(f" - {sug}")
