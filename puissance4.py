import os
from colors import *


# Ici, X correspond à la colonne, et Y à la ligne.
class Game:
    def __init__(self):
        # On initialise les cases prisent.
        self.pattern = []

        # On dit c'est au tour de quel joueur.
        self.tour = 0

        # On initialise le nom des joueurs
        self.players = []

        # On initialise les couleurs en console.
        self.colors = termColors()

    def clear_console(self):
        # Si le nom de l'os est égale à nt (soit windows), on clear avec la commande windows, sinon on clear avec la commande linux.
        os.system('cls') if os.name == "nt" else os.system('clear')

    def affiche_grille(self):
        '''
            On initialise la variable grille qui correspond à une string qu'on va remplir.
            A chaque Y, on rajoute une ligne de grille complète pour séparer le tableau et avoir mes valeurs X et Y des jeutons
            simplifiés.
        '''
        grille = ''
        for hauteur in range(0, 6):
            grille += "\n+---+---+---+---+---+---+---+\n"
            for largeur in range(0, 7):
                player = self.get_case_statut(largeur, hauteur)

                # Si la case n'est pas prise, alors on remplace la case du joueur par un espace vide.
                if not player:
                    player = ' '

                else:
                    # Sinon, on prend l'id du joueur grâce à son signe.
                    player = self.players[0 if player['player'] == 'X' else 1]['color'] + player[
                        'player'] + self.colors.reset

                grille += "| %s " % player
            grille += '|'

        # On ajoute la dernière ligne & le numéro des colonnes.
        grille += '\n+---+---+---+---+---+---+---+'
        grille += '\n  1   2   3   4   5   6   7\n\n'
        return grille;

    def grille_init(self):
        self.pattern = []
        grille = self.affiche_grille()
        return grille;

    def colonne_libre(self, colonne):
        '''
        En mettant not une première fois, on converti notre réponse Boolean OU Object en Boolean obligatoirement.
        Si la réponse était égale à False, alors elle se transforme en True, et si elle était en Object, elle se transforme en false.
        
        On prend la ligne numéro 9, soit celle la plus haute afin de savoir si la case la plus en haut est prise. Si c'est le cas, la colonne
        est pleine.
        '''
        return not self.get_case_statut(colonne, 0)

    def get_case_statut(self, colonne, ligne):
        pattern = self.pattern
        '''
        On regarde dans toutes les cases prises si il n'y en a pas une avec laquelle, le y et le x match avec celui qu'on cherche. Si c'est
        le case, on retourne ses valeurs. Sinon, on return False.
        '''
        for i in range(0, len(pattern)):
            if pattern[i]['y'] == ligne and pattern[i]['x'] == colonne:
                return self.pattern[i]

        return False

    def place_jeton(self, colonne, joueur):
        # On prend le signe du joueur
        signe = self.players[joueur]['signe']

        # On cherche la colonne la plus basse libre, et on lui attribue la valeur du joueur.
        for i in range(6):
            if not (self.get_case_statut(colonne, 5 - i)):
                self.pattern.append({
                    'x': colonne,
                    'y': 5 - i,
                    'player': signe
                })
                return self

    def init_players(self):

        # On demande les noms des joueurs.
        player1 = input("Quel est le nom du premier joueur ? ")
        player2 = input("Quel est le nom du second joueur ? ")

        # On ajoute les joueurs à notre tableau de joueurs.
        self.players.extend([{
            'name': player1,
            'signe': 'X',
            'color': self.colors.jaune
        }, {
            'name': player2,
            'signe': 'O',
            'color': self.colors.cyan
        }])
        return self

    def verticale(self, joueur):

        # On vérifie si  les cases on 4 cases de haut d'affilés.
        case_affiliees = 0
        for largeur in range(0, 7):
            for hauteur in range(0, 6):
                case = self.get_case_statut(largeur, hauteur)

                if case and case['player'] == self.players[joueur]['signe']:
                    case_affiliees += 1
                else:
                    case_affiliees = 0

                if case_affiliees > 3:
                    return True

        return False

    def horizontale(self, joueur):

        # On vérifie si  les cases on 4 cases de large d'affilés.
        case_affiliees = 0
        for hauteur in range(0, 6):
            for largeur in range(0, 7):
                case = self.get_case_statut(largeur, hauteur)

                if case and case['player'] == self.players[joueur]['signe']:
                    case_affiliees += 1
                else:
                    case_affiliees = 0

                if case_affiliees > 3:
                    return True

        return False

    def diagonale(self, joueur):
        # Grâce à mon beau schéma (c'est faux), j'ai réussi à éliminer les cases pour les 4 directions (NE, NW, SE, SW) qui ne servaient à rien dans mes boucles. Si on ne rentre
        # Pas dans une condition qui dit que la case est inutile à vérifier, on ne la vérifie pas.
        # Sinon, on vérifie les 4 cases en diagonales pour savoir si elles sont remplies par le même joueur ou non.
        for hauteur in range(6):
            for largeur in range(7):
                case = self.get_case_statut(largeur, hauteur)
                if case and case['player'] == self.players[joueur]['signe']:
                    alignee = 1

                    for i in range(4):

                        case_decalee = False

                        # De bas en haut vers la gauche (NW)
                        if largeur > 2 and hauteur > 2:
                            case_decalee = self.get_case_statut(largeur - i - 1, hauteur - i - 1)

                        # De bas en haut vers la droite (NE)
                        elif largeur < 4 and hauteur > 2:
                            case_decalee = self.get_case_statut(largeur + i + 1, hauteur - i - 1)

                        if case_decalee and case_decalee['player'] == self.players[joueur]['signe']:
                            alignee += 1
                        else:
                            # Si on détecte que une case ne respecte pas les conditions, on arrête la boucle pour éviter des itérations
                            # en trop.
                            break;

                        if alignee > 3:
                            return True

        return False

    def gagne(self, joueur):
        return self.horizontale(joueur) or self.verticale(joueur) or self.diagonale(joueur);

    def egalite(self):
        colomn_occupees = 0
        for i in range(7):
            if not self.colonne_libre(i):
                colomn_occupees += 1
        return colomn_occupees > 6

    def tour_joueur(self, joueur):
        player = self.players[joueur]['name']

        # Garde en mémoire la phrase et évite de la regénérer à chaque fois.
        question = "%s Dans quel colonne souhaites-tu mettre ton jeton ? (Entre 1 et 7) " % player
        colonne = int(input(question)) - 1

        while not self.colonne_libre(colonne) or (colonne < 0 or colonne > 6):
            print("La colonne séléctionnée est pleine.")
            colonne = int(input(question)) - 1

        self.place_jeton(colonne, joueur)
        print(self.affiche_grille())
        self.tour = 1 if self.tour == 0 else 0
