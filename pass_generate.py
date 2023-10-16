import random
import string


def generate_password(num,strength):
   
            if strength == "strong":
                characters = string.ascii_letters + string.digits + string.punctuation
            elif strength == "intermediate":
                characters = string.ascii_letters + string.digits
            elif strength == "weak":
                 characters = string.ascii_lowercase

            length=int(num)
            password = "".join(random.choice(characters) for _ in range(length))
            
            return password