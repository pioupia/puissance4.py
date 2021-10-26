# -*-coding:Latin-1 -*
# La ligne au dessus permet de mettre des caractères spéciaux dans la console.

from puissance4 import *
from colors import *

puissance4 = Game()
puissance4.clear_console()
colors = termColors()
puissance4.init_players()
puissance4.clear_console()
textVS = (colors.gras + colors.underline + colors.jaune + "%s VS %s !" % (
puissance4.players[0]['name'], puissance4.players[1]['name']) + colors.reset).center(40)

print(textVS)
print(puissance4.grille_init())

while not (puissance4.gagne(0) or puissance4.gagne(1) or puissance4.egalite()):
    puissance4.tour_joueur(puissance4.tour)
    puissance4.clear_console()
    print(textVS)
    print(puissance4.affiche_grille())

if puissance4.gagne(0):
    print((colors.gras + colors.underline + colors.jaune + puissance4.players[0][
        'name'] + " a gagné !" + colors.reset).center(40))
elif puissance4.egalite():
    print(
        (colors.gras + colors.underline + colors.rouge + "Égalité. Aucun joueur n'a gagné." + colors.reset).center(40))

else:
    print((colors.gras + colors.underline + colors.jaune + puissance4.players[1][
        'name'] + " a gagné !" + colors.reset).center(40))

print('\n\n')
