import requests
import secrets

def get_wordlist():
    try:
        URL = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"
        response = requests.get(URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching wordlist: {e}")
        return None
    
def parse_wordlist(wordlist):
    wordmap = {}
    for line in wordlist.splitlines():
        if line.strip():
            wordmap[line.split()[0]] = line.split()[1]
    return wordmap

def generate_password(wordmap, length=6, sequence=None):
    if not sequence:
        return ' '.join(secrets.choice(list(wordmap.values())) for _ in range(length))
    else:
        return ' '.join(wordmap[sequence[i]] for i in range(length))

def main():
    wordlist = get_wordlist()
    if wordlist:
        wordmap = parse_wordlist(wordlist)
        sequence = None
        print("*" * 50)
        print("Welcome to Diceware Password Generator!")
        print("*" * 50)
        pass_length = int(input("Enter the length of the password you want to generate: "))
        print("Would you like to enter a sequence of numbers to generate a password?")
        if input("Enter 'y' for yes, 'n' for no: ") == 'y':
            sequence = []
            for i in range(pass_length):
                print(f"Enter the {i+1}th number of the sequence: ")
                try:
                    num = input()
                    if any(c not in '123456' for c in num):
                        print("Invalid input. Please enter a number between 1 and 6.")
                        i -= 1
                    else:
                        sequence.append(num)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    i -= 1
        password = generate_password(wordmap, pass_length, sequence)
        print(f"Generated password: {password}")
    else:
        print("Failed to fetch wordlist")

if __name__ == "__main__":
    main()