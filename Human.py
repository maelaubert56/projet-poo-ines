import random
from Element import Element


class Human(Element):
    """
    Represents a Human entity in the simulation.
    
    Features:
    - Age progression
    - Nationality and identity
    - Life expectancy and natural death
    - Age-based behavior
    
    Class Attributes:
        LIFE_EXPECTANCY (int): Age at which natural death chance begins
        __count (int): Total number of Human instances created
    """
    __count = 0
    LIFE_EXPECTANCY = 50  # Âge à partir duquel la mortalité augmente

    @classmethod
    def get_count(cls):
        """Return the total number of Human instances created."""
        return cls.__count

    def __init__(self, first_names, last_name, alpha_code2, greetings, majority=18, kinds=['Human'], name='Human', char_repr='H', sound='Hi'):
        """
        Initialize a Human instance.
        
        Args:
            first_names (list): List of first names
            last_name (str): Family name
            alpha_code2 (str): Two-letter country code
            greetings (str): Greeting message
            majority (int, optional): Age of majority. Defaults to 18
        """
        super().__init__(char_repr)
        self.kinds = kinds
        self.name = name
        self.sound = sound
        self.__full_name = " ".join(map(str,[" ".join(first_names),last_name]))
        self.__age = 0
        self.__majority = majority
        self.__greetings = greetings
        self.__nationality = alpha_code2.upper()

        Human.__count +=1


    def get_age(self):
        """Return the age of the Human instance."""
        return self.__age
    def set_age(self, new_age):
        """Set a new age for the Human instance."""
        self.__age = new_age

    def get_full_name(self):
        """Return the full name of the Human instance."""
        return self.__full_name
    def set__full_name(self,new_full_name):
        """Set a new full name for the Human instance."""
        self.__full_name = new_full_name

    def get_majority(self):
        """Return the age of majority for the Human instance."""
        return self.__majority
    def set_majority(self, new_majority):
        """Set a new age of majority for the Human instance."""
        self.__majority = new_majority

    def get_greetings(self):
        """Return the greeting message of the Human instance."""
        return self.__greetings
    def set_greetings(self, new_greetings):
        """Set a new greeting message for the Human instance."""
        self.__greetings = new_greetings

    def get_nationality(self):
        """Return the nationality of the Human instance."""
        return self.__nationality
    def set_nationality(self, new_nationality):
        """Set a new nationality for the Human instance."""
        self.__nationality = new_nationality


    def is_adult(self):
        """
        Return 'True' if the age of majority is reached. 'False' otherwise.
        """
        if self.__age >= self.__majority:
            return '(majeur)'
        return '(mineur)'

    def get_info(self):
        """
        Return a string indicating all the information of the Human instance.
        """
        return ' - '.join([
            f"IdentitÃ© : {self.__full_name}",
            f"NationalitÃ© : {self.__nationality}",
            f"Age : {self.__age} ans {self.is_adult()}"])

    def ageing(self, years=1):
        """
        Add the specified number of years to the age.
        
        Args:
            years (int, optional): Number of years to add. Defaults to 1.
        """
        self.__age += years

    def get_shout(self):
        """
        Return a string based on the age:
        - up to 1 year: "Ouin ouin"
        - up to 2 years: "Areuh baba gaga"
        - up to 3 years: greetings with shuffled letters
        - from 3 years: normal greetings
        """
        if self.__age >= 4:
            return f"Je mâ€™appelle {Human.get_full_name(self)} et jâ€™ai la nationalitÃ© {self.__nationality.lower()}. {self.__greetings} !"
        if self.__age >= 3:
            return self.__greetings
        if self.__age >= 2:
            babbling = list(self.__greetings)
            random.shuffle(babbling)
            return ''.join(babbling)
        if self.__age >= 1:
            return 'Areuh baba gaga'
        return 'Ouin ouin'
