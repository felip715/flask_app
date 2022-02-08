import re
def validar_mail(email: str) -> bool:
    emailRegex = r'\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b'
    match = re.search(emailRegex, email)
    if match:
        print(email + ' es una dirección válida.')
        return True
    else:
        print(email + ' no es una dirección válida.')
        return False