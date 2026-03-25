import turtle
import time
import random
from random import randint
import interface


def move_turtle(tortue):
    """
    Déplace la tortue dans la fenêtre.
    :param tortue: Instance de la tortue
    :return: Aucun
    """
    speed = calculate_speed(tortue)
    tortue.forward(speed)


def bounce(tortue, width, height):
    """
    Faire rebondir lorsqu'elle atteint une bordure.
    :param tortue: Instance de la tortue
    :param width: Largeur de la fenêtre
    :param height: Hauteur de la fenêtre
    :return: Aucun
    """
    x, y = tortue.position()
    heading = tortue.heading()
    radius = turtle_to_radius(tortue)
    if x < - width // 2 - 80 + radius:
        tortue.setheading(180 - heading)
        tortue.setx(- width // 2 - 80 + radius)
    elif x > width // 2 - 80 - radius:
        tortue.setheading(180 - heading)
        tortue.setx(width // 2 - 80 - radius)
    if y < - height // 2 + radius:
        tortue.setheading(360 - heading)
        tortue.sety(- height // 2 + radius)
    elif y > height // 2 - radius:
        tortue.setheading(360 - heading)
        tortue.sety(height // 2 - radius)


def turtle_to_radius(tortue):
    """
    Calcule et retourne le rayon de la tortue en pixels.
    :param tortue: Instance de la tortue
    :return: Rayon de la tortue en pixels
    """
    size = tortue.shapesize()[0] * 20
    return size / 2


def calculate_speed(tortue):
    """
    Calcule la vitesse de déplacement de la tortue en fonction de sa taille.
    :param tortue: Instance de la tortue
    :return: Vitesse de déplacement
    """
    radius = turtle_to_radius(tortue)
    speed = (5 - radius // 20)
    return speed


def size_to_scale(pixels):
    """
    Convertit la taille en pixels en échelle de taille de tortue.
    :param pixels: Taille en pixels
    :return: Échelle de taille de la tortue
    """
    size_scale = pixels / 20
    return size_scale


def check_collision(t1, t2):
    """
    Vérifie si deux tortues se chevauchent.
    :param t1: Première tortue
    :param t2: Deuxième tortue
    :return: True si les tortues se chevauchent, sinon False
    """
    distance = t1.distance(t2)
    radius1 = turtle_to_radius(t1)
    radius2 = turtle_to_radius(t2)
    return distance < radius1 + radius2


def eat(tortues_creation):
    """
    Gère les collisions entre les tortues.
    :param tortues_creation: Liste des tortues
    :return: Liste mise à jour des tortues
    """
    for t1 in tortues_creation:
        for t2 in tortues_creation:
            if t1 != t2 and check_collision(t1, t2):
                radius1 = turtle_to_radius(t1)
                radius2 = turtle_to_radius(t2)
                if radius1 > radius2:
                    tortues_a_supprimer.append(t2)
                    t2.clear()
                    if radius1 < 40:
                        new_scale = size_to_scale((radius1 + radius2 // 2) * 2)
                        t1.shapesize(new_scale)
                    if t1 not in score_tortues:
                        score_tortues[t1] = 0
                    score_tortues[t1] += 5
                elif radius2 > radius1:
                    tortues_a_supprimer.append(t1)
                    t1.clear()
                    if radius2 < 40:
                        new_scale = size_to_scale((radius2 + radius1 // 2) * 2)
                        t2.shapesize(new_scale)
                    if t2 not in score_tortues:
                        score_tortues[t2] = 0
                    score_tortues[t2] += 5

    for t in tortues_a_supprimer:
        if t in tortues_creation:
            t.hideturtle()
            tortues_creation.remove(t)

    return [t for t in tortues_creation if t not in tortues_a_supprimer]


def draw_border(width, height):
    """
    Dessine une bordure autour de la fenêtre.
    :param width: Largeur de la fenêtre en pixels
    :param height: Hauteur de la fenêtre en pixels
    :return: Aucun
    """
    border_turtle = turtle.Turtle()
    border_turtle.penup()
    border_turtle.goto(-width // 2 - 80, -height // 2)
    border_turtle.pendown()
    border_turtle.pensize(1)
    for _ in range(2):
        border_turtle.forward(width)
        border_turtle.left(90)
        border_turtle.forward(height)
        border_turtle.left(90)
    border_turtle.hideturtle()


def ecart_points_tortues(p1, p2):
    """
    Vérifie si une tortue et un point se chevauchent.
    :param p1: tortue
    :param p2: point
    :return: True si la tortue et le point se chevauchent, sinon False
    """
    distance = p1.distance(p2)
    radiusp1 = turtle_to_radius(p1)
    radiusp2 = turtle_to_radius(p2)
    return distance < radiusp1 + radiusp2


def eat_points(tortues_creation, points):
    """
    Gère les collisions entre les tortues et les points.
    :param tortues_creation: Liste des tortues
    :param points: Liste des points
    :return: Liste mise à jour des points
    """
    for t1 in tortues_creation:
        for p2 in points:
            radiust1 = turtle_to_radius(t1)
            radiusp2 = turtle_to_radius(p2)
            if t1 != p2 and ecart_points_tortues(t1, p2):
                p2.hideturtle()
                points.remove(p2)
                if radiust1 < 40:
                    new_scale = size_to_scale((radiust1 + radiusp2) * 2)
                    t1.shapesize(new_scale)
                if t1 not in score_tortues:
                    score_tortues[t1] = 0
                score_tortues[t1] += 1
    return points


def chase(tortue, tortues_creation, points):
    """
    Ajuste la direction de la tortue en fonction des tortues voisines et des points.
    Les petites tortues fuient les grosses et les grosses poursuivent les petites.
    Les tortues poursuivent aussi les points.
    :param tortue: Instance de la tortue
    :param tortues_creation: Liste des tortues
    :param points: Liste des points
    :return: Aucun
    """
    closest_tortue = None
    closest_point = 0
    min_distance_tortue = 9999999
    min_distance_point = 9999999

    for other_tortue in tortues_creation:
        if tortue != other_tortue:
            distance = tortue.distance(other_tortue)
            if distance < min_distance_tortue:
                closest_tortue = other_tortue
                min_distance_tortue = distance

    for point in points:
        distance = tortue.distance(point)
        if distance < min_distance_point:
            closest_point = point
            min_distance_point = distance

    if closest_point and (closest_tortue == 0 or min_distance_point < min_distance_tortue):
        angle = tortue.towards(closest_point)
        tortue.setheading(angle)
    elif closest_tortue:
        radius_tortue = turtle_to_radius(tortue)
        radius_other = turtle_to_radius(closest_tortue)
        if radius_tortue < radius_other:
            angle = tortue.towards(closest_tortue) + 180  # fuis
            tortue.setheading(angle)
        elif radius_tortue > radius_other:
            angle = tortue.towards(closest_tortue)  # attaque
            tortue.setheading(angle)


def ecart_carres_tortues(c1, c2):
    """
    Vérifie si une tortue et un carré se chevauchent.
    :param c1: tortue
    :param c2: carré
    :return: True si la tortue et le carré se chevauchent, sinon False
    """
    distance = c1.distance(c2)
    radiusc1 = turtle_to_radius(c1)
    radiusc2 = turtle_to_radius(c2)
    return distance < radiusc1 + radiusc2


tortues_a_supprimer = []


def diviser_tortue(tortues_creation, carres):
    """
    Gère les collisions entre les tortues et les carres.
    :param tortues_creation: Liste des tortues
    :param carres: Liste des carres
    :return: Liste mise à jour des carres
    """
    for c1 in tortues_creation:
        for c2 in carres:
            radiusc1 = turtle_to_radius(c1)
            radiusc2 = turtle_to_radius(c2)
            if ecart_carres_tortues(c1, c2) and radiusc1 > radiusc2:
                tortues_a_supprimer.append(c1)
                x, y = c2.position()
                tortue = turtle.Turtle()
                tortue.shape("turtle")
                tortue.fillcolor(c1.fillcolor())
                tortue.pencolor(tortue.fillcolor())
                new_scale = size_to_scale(radiusc1 * 0.80)
                tortue.shapesize(new_scale)
                tortue.penup()
                tortue.left(randint(0, 360))
                tortue.goto(x + 2 * radiusc2, y + 2 * radiusc2)
                tortue.name = c1.name
                tortue.write(tortue.name)
                tortues_creation.append(tortue)
                score_tortues[tortue] = score_tortues[c1] // 3
                tortue2 = turtle.Turtle()
                tortue2.shape("turtle")
                tortue2.fillcolor(c1.fillcolor())
                tortue2.pencolor(tortue2.fillcolor())
                new_scale = size_to_scale(radiusc1 * 0.80)
                tortue2.shapesize(new_scale)
                tortue2.penup()
                tortue2.left(randint(0, 360))
                tortue2.goto(x - 2 * radiusc2, y - 2 * radiusc2)
                tortue2.name = c1.name
                tortue2.write(tortue2.name)
                tortues_creation.append(tortue2)
                score_tortues[tortue2] = score_tortues[c1] // 3

    for t in tortues_a_supprimer:
        t.clear()
        if t in tortues_creation:
            t.hideturtle()
            tortues_creation.remove(t)

    return [t for t in tortues_creation if t not in tortues_a_supprimer]


score_tortues = {}


def main(width, height, n):
    """
    Crée la fenêtre Turtle et tous les composants nécessaires pour configurer le jeu et faire bouger les tortues.
    :param width: Largeur de la fenêtre en pixels
    :param height: Hauteur de la fenêtre en pixels
    :param n: Nombre de tortues
    :return: Aucun
    """
    window = turtle.Screen()
    window.title("Projet A1 2024")
    window.setup(width=width, height=height)
    window.tracer(0)
    draw_border(width, height)
    score_turtle = turtle.Turtle()
    tortues_creation = []
    noms = ["trecia", "clara", "tessa", "lucie", "tuan", "sofiane", "thomas", "yanis", "eliott", "jules", "hugo",
            "leonard", "lexie", "eileen", "marceau", "philibert", "matthieu", "tom", "theo", "arthur", "louis", "adam"]
    for i in range(n):
        tortue = turtle.Turtle()
        tortue.shape("turtle")
        tortue.fillcolor(random.choice(
            ['lightblue', 'lightgreen', 'lightcoral', 'yellow', 'purple', 'red', 'blue', 'cyan', 'magenta', 'black',
             'pink']))
        tortue.pencolor(tortue.fillcolor())  # border color
        tortue.shapesize(size_to_scale(randint(5, 10)))
        tortue.penup()
        tortue.left(randint(0, 360))
        tortue.goto(randint(-width // 2, width // 2 - 80), randint(-height // 2, height // 2))
        tortue.name = random.choice(noms)
        noms.remove(tortue.name)
        tortues_creation.append(tortue)

    points_creation = []
    for p in range(50):
        point = turtle.Turtle()
        point.shape("circle")
        point.pencolor('orange')
        point.fillcolor('orange')
        point.shapesize(1 / 2)
        point.penup()
        point.goto(randint(- width // 2, width // 2 - 80), randint(- height // 2 + 10, height // 2 - 10))
        points_creation.append(point)

    carres_creation = []
    for c in range(10):
        carre = turtle.Turtle()
        carre.shape("square")
        carre.pencolor('green')
        carre.fillcolor('green')
        carre.shapesize(2)
        carre.penup()
        carre.goto(randint(- width // 2 - 70, width // 2 - 80), randint(- height // 2 + 10, height // 2 - 10))
        carres_creation.append(carre)

    for tortue in tortues_creation:
        score_tortues[tortue] = 0

    while True:
        window.update()  # Rafraîchissement de l'affichage
        score_turtle.clear()
        # Ajouter un entête au tableau
        score_turtle.penup()
        score_turtle.goto(width // 2 + 80, height // 2 - 25)
        score_turtle.write("Tableau de scores", align="right", font=("Arial", 12, "bold"))
        row = 1
        if tortue not in score_tortues:
            score_tortues[tortue] = 0
        for tortue in tortues_creation:
            if tortue in score_tortues:
                score_turtle.goto(width // 2 + 80, height // 2 - 25 - row * 20)
                score_turtle.write(f"{tortue.name}: {score_tortues.get(tortue)}", align="right", font=("Arial", 12,
                                                                                                       "normal"))
                row += 1
                score_turtle.hideturtle()
            tortue.clear()
            move_turtle(tortue)
            bounce(tortue, width, height)
            eat_points(tortues_creation, points_creation)
            chase(tortue, tortues_creation, points_creation)
            eat(tortues_creation)
            for i in range(1):
                if random.random() <= 0.015:
                    point = turtle.Turtle()
                    point.shape("circle")
                    point.pencolor('orange')
                    point.fillcolor('orange')
                    point.shapesize(1 / 2)
                    point.penup()
                    point.goto(randint(- width // 2, width // 2 - 80), randint(- height // 2 + 10, height // 2 - 10))
                    points_creation.append(point)
            diviser_tortue(tortues_creation, carres_creation)

            # Afficher le nom de la tortue au-dessus d'elle
            if tortue in tortues_creation:
                tortue.setx(tortue.xcor() + turtle_to_radius(tortue) / 1.3)
                tortue.sety(tortue.ycor() + turtle_to_radius(tortue) / 1.3)
                tortue.write(tortue.name)
                tortue.setx(tortue.xcor() - turtle_to_radius(tortue) / 1.3)
                tortue.sety(tortue.ycor() - turtle_to_radius(tortue) / 1.3)

        time.sleep(0.002)  # Délai de rafraîchissement de l'affichage, ici 50 millisecondes
