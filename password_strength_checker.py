import re
import getpass
import string

class PasswordStrengthChecker:
    def __init__(self):
        self.common_patterns = [
            '123', 'abc', 'password', 'qwerty', 'letmein', 'welcome',
            '111', '000', 'iloveyou', 'admin', 'user', 'login'
        ]

    def check_length(self, pwd):
        return len(pwd) >= 8

    def check_recommended_length(self, pwd):
        return len(pwd) >= 12

    def check_lower(self, pwd):
        return bool(re.search(r'[a-z]', pwd))

    def check_upper(self, pwd):
        return bool(re.search(r'[A-Z]', pwd))

    def check_number(self, pwd):
        return bool(re.search(r'[0-9]', pwd))

    def check_special(self, pwd):
        return any(char in string.punctuation for char in pwd)

    def check_common_patterns(self, pwd):
        pwd_lower = pwd.lower()
        return not any(pattern in pwd_lower for pattern in self.common_patterns)

    def check_repetition(self, pwd):
        return not bool(re.search(r'(.)\1{2,}', pwd))

    def evaluate(self, pwd):
        criteria = [
            self.check_length(pwd),
            self.check_recommended_length(pwd),
            self.check_lower(pwd),
            self.check_upper(pwd),
            self.check_number(pwd),
            self.check_special(pwd),
            self.check_common_patterns(pwd),
            self.check_repetition(pwd)
        ]
        score = sum(criteria)
        suggestions = []
        if not criteria[0]:
            suggestions.append("Make it at least 8 characters.")
        if not criteria[1]:
            suggestions.append("12+ characters recommended.")
        if not criteria[2]:
            suggestions.append("Add lowercase letters.")
        if not criteria[3]:
            suggestions.append("Add uppercase letters.")
        if not criteria[4]:
            suggestions.append("Add digits.")
        if not criteria[5]:
            suggestions.append("Add symbols or special characters.")
        if not criteria[6]:
            suggestions.append("Avoid common patterns (e.g. 123, 'password').")
        if not criteria[7]:
            suggestions.append("Don't repeat characters too much.")
        return {
            'score': score,
            'total': len(criteria),
            'criteria': criteria,
            'suggestions': suggestions
        }

def rating(score, total):
    percent = score / total * 100
    if percent == 100:
        return "Very Strong"
    elif percent >= 87.5:
        return "Strong"
    elif percent >= 62.5:
        return "Moderate"
    elif percent >= 37.5:
        return "Weak"
    else:
        return "Very Weak"

if __name__ == "__main__":
    checker = PasswordStrengthChecker()
    print("=== Password Strength Checker ===")
    print("Enter 'quit' to exit\n")

    while True:
        pwd = getpass.getpass("Enter password to check: ")
        if pwd.lower() == 'quit':
            print("Bye!")
            break
        result = checker.evaluate(pwd)
        print(f"\n--- Results for your password ---")
        print(f"Score: {result['score']}/{result['total']} ({round(result['score']/result['total']*100)}%)")
        print(f"Rating: {rating(result['score'], result['total'])}")
        if result['score'] == result['total']:
            print("\n✅ Excellent! Your password meets all criteria.")
        else:
            print("\nSuggestions to improve:")
            for sug in result['suggestions']:
                print(f" - {sug}")
        print("")
