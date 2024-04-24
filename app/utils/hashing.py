import random
import string
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def generate_random_password(length=12):
        """Generate a random password."""

        num_letters = random.randint(2, 4)
        num_digits = random.randint(2, 4)
        num_symbols = length - num_letters - num_digits

        password_list = (
            [random.choice(string.ascii_letters) for _ in range(num_letters)]
            + [random.choice(string.digits) for _ in range(num_digits)]
            + [random.choice(string.punctuation) for _ in range(num_symbols)]
        )

        random.shuffle(password_list)

        random_password = "".join(password_list)

        return random_password
