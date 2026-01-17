class Tank:
    # Types d'armure valides avec son bonus de protection
    VALID_ARMOR_TYPES = {
        'chobham': 100,
        'composite': 50,
        'ceramic': 50
    }

    def __init__(self, armor, penetration, armor_type, name=None):
        # Initialise un tank avec :
        # - armor : valeur de l'armure de base
        # - penetration : puissance de tir
        # - armor_type : type d'armure ('chobham', 'composite', 'ceramic')
        # - name : nom du tank

        try:
            # Test si l'armure est valide
            bonus = self.VALID_ARMOR_TYPES[armor_type]
        except KeyError:
            # Si le type d'armure n'est pas dans le dictionnaire
            print(f"Erreur : type d'armure invalide '{armor_type}'")
            raise  # Exception pour stopper la création

        self.armor = armor
        self.penetration = penetration
        self.armor_type = armor_type
        self.name = name or "Tank"

    # Changer le nom du tank
    def set_name(self, name):
        self.name = name

    # Calcule si le tank est vulnérable face à un attaquant
    def vulnerable(self, attacker):
        real_armor = self.armor + self.VALID_ARMOR_TYPES.get(self.armor_type, 0)
        return real_armor <= attacker.penetration

    # Échange l'armure du tank avec un autre tank
    def swap_armor(self, other_tank):
        self.armor, other_tank.armor = other_tank.armor, self.armor

    def __repr__(self):
        return self.name.replace(' ', '-').lower()


# Création de tanks
m1_1 = Tank(600, 670, 'chobham', name="M1_1")
m1_2 = Tank(620, 670, 'chobham', name="M1_2")

# Test vulnérabilité
if m1_1.vulnerable(m1_2):
    print('Vulnerable contre M1_2')

# Échange des armures
m1_1.swap_armor(m1_2)

# Création de 5 tanks de test
tanks = []
test_results = []

for idx in range(5):
    tank = Tank(400, 400, 'composite')
    tank.set_name(f"Tank{idx}_Small")
    tanks.append(tank)

    # Calcul vulnérabilité face à m1_1
    test_results.append(tank.vulnerable(m1_1))

# Vérifie si un tank de la liste est safe
def test_tank_safe(attacker, tanks_to_test):
    at_least_one_safe = any(not t.vulnerable(attacker) for t in tanks_to_test)
    if at_least_one_safe:
        print("At least one tank is safe")
    else:
        print("No tank is safe")


# Test final
test_tank_safe(m1_1, tanks)
