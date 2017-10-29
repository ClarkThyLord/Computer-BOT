from src.vainglory_work import tools
from PIL import Image, ImageFont, ImageDraw
import random
import math
import traceback
import config


# Transforms locations
def mapX(x):
    """Given x cords from Vainglory map transform them relative to our map."""
    xC = 1242

    return x * 13.3 + xC


# Transforms locations
def mapY(y):
    """Given y cords from Vainglory map transform them relative to our map."""
    yC = 317

    return y * 13.4 + yC


def giveX2(x1, distance, angle):
    """Given x1, distance and a angle give x2."""

    result = int((distance * math.cos(angle / 180 * math.pi)) + x1)

    # FOR DEBUGGING
    # print("X1: " + str(x1) + " |DISTANCE: " + str(distance) + " |ANGLE: " + str(angle))
    # print("X2: " + str(result))

    return result


def giveY2(y1, distance, angle):
    """Given y1, distance and a angle give y2."""

    result = int((distance * math.sin(angle / 180 * math.pi)) + y1)

    # FOR DEBUGGING
    # print("Y1: " + str(y1) + " |DISTANCE: " + str(distance) + " |ANGLE: " + str(angle))
    # print("Y2: " + str(result))

    return result


# Add a kraken icon to the given img
def markKraken(image, cords, color="grey"):
    """
    Mark a kraken icon on a image.
    """

    try:

        # Size of image parts
        sizeX = 22.5
        sixeY = 23.5

        if color == "grey":  # Open the image for kraken color grey
            kraken = Image.open(config.directory + "//res//vainglory//mapping//kraken_grey.png")

        elif color == "blue":  # Open the image for kraken color blue
            kraken = Image.open(config.directory + "//res//vainglory//mapping//kraken_blue.png")

        elif color == "red":  # Open the image for kraken color red
            kraken = Image.open(config.directory + "//res//vainglory//mapping//kraken_red.png")

        else:  # Open the image for kraken color grey
            kraken = Image.open(config.directory + "//res//vainglory//mapping//kraken_grey.png")

        # Scale cords to map size
        x = mapX(cords[0])
        y = mapY(cords[2])

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("KRAKEN:")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(kraken, (x1, y1, x2, y2), kraken)

        # Close used img
        kraken.close()

        return image

    except Exception as e:
        print("KRAKEN MARK ERROR:\n" + str(e))


# Add a circle icon to the given img
def markCircle(image, cords, color="grey"):
    """
    Mark a circle icon on a image.
    """

    try:

        # Size of image parts
        sizeX = 16
        sixeY = 16

        if color == "grey":  # Open the image for circle color grey
            circle = Image.open(config.directory + "//res//vainglory//mapping//circle_grey.png")

        elif color == "blue":  # Open the image for circle color blue
            circle = Image.open(config.directory + "//res//vainglory//mapping//circle_blue.png")

        elif color == "red":  # Open the image for circle color red
            circle = Image.open(config.directory + "//res//vainglory//mapping//circle_red.png")

        else:  # Open the image for circle color grey
            circle = Image.open(config.directory + "//res//vainglory//mapping//circle_grey.png")

        # Scale cords to map size
        x = mapX(cords[0])
        y = mapY(cords[2])

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("CIRCLE:")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(circle, (x1, y1, x2, y2), circle)

        # Close used img
        circle.close()

        return image

    except Exception as e:
        print("CIRCLE MARK ERROR:\n" + str(e))


# Add a crystal icon to the given img
def markCrystal(image, cords, color="grey"):
    """
    Mark a crystal icon on a image.
    """

    try:

        # Size of image parts
        sizeX = 27.5
        sixeY = 40

        if color == "grey":  # Open the image for crystal color grey
            crystal = Image.open(config.directory + "//res//vainglory//mapping//crystal_grey.png")

        elif color == "blue":  # Open the image for crystal color blue
            crystal = Image.open(config.directory + "//res//vainglory//mapping//crystal_blue.png")

        elif color == "red":  # Open the image for crystal color red
            crystal = Image.open(config.directory + "//res//vainglory//mapping//crystal_red.png")

        else:  # Open the image for crystal color grey
            crystal = Image.open(config.directory + "//res//vainglory//mapping//crystal_grey.png")

        # Scale cords to map size
        x = mapX(cords[0])
        y = mapY(cords[2])

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("CRYSTAL:")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(crystal, (x1, y1, x2, y2), crystal)

        # Close used img
        crystal.close()

        return image

    except Exception as e:
        print("CRYSTAL MARK ERROR:\n" + str(e))


# Add a dot icon to the given img
def markDot(image, cords, color="grey"):
    """
    Mark a dot icon on a image.
    """

    try:

        # Size of image parts
        sizeX = 7
        sixeY = 7

        if color == "grey":  # Open the image for dot color grey
            dot = Image.open(config.directory + "//res//vainglory//mapping//dot_grey.png")

        elif color == "blue":  # Open the image for dot color blue
            dot = Image.open(config.directory + "//res//vainglory//mapping//dot_blue.png")

        elif color == "red":  # Open the image for dot color red
            dot = Image.open(config.directory + "//res//vainglory//mapping//dot_red.png")

        else:  # Open the image for dot color grey
            dot = Image.open(config.directory + "//res//vainglory//mapping//dot_grey.png")

        # Scale cords to map size
        x = mapX(cords[0])
        y = mapY(cords[2])

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("DOT:")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(dot, (x1, y1, x2, y2), dot)

        # Close used img
        dot.close()

        return image

    except Exception as e:
        print("DOT MARK ERROR:\n" + str(e))


# Add a flag icon to the given img
def markFlag(image, cords, color="grey"):
    """
    Mark a flag icon on a image.
    """

    try:

        # Size of image parts
        sizeX = 13
        sixeY = 13

        if color == "grey":  # Open the image for flag color grey
            flag = Image.open(config.directory + "//res//vainglory//mapping//flag_grey.png")

        elif color == "blue":  # Open the image for flag color blue
            flag = Image.open(config.directory + "//res//vainglory//mapping//flag_blue.png")

        elif color == "red":  # Open the image for flag color red
            flag = Image.open(config.directory + "//res//vainglory//mapping//flag_red.png")

        else:  # Open the image for flag color grey
            flag = Image.open(config.directory + "//res//vainglory//mapping//flag_grey.png")

        # Scale cords to map size
        x = mapX(cords[0])
        y = mapY(cords[2])

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("FLAG:")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(flag, (x1, y1, x2, y2), flag)

        # Close used img
        flag.close()

        return image

    except Exception as e:
        print("FLAG MARK ERROR:\n" + str(e))


# Add a turret icon to the given img
def markTurret(image, cords, color="grey"):
    """
    Mark a turret icon on a image.
    """

    try:

        # Size of image parts
        sizeX = 18
        sixeY = 18

        if color == "grey":  # Open the image for turret color grey
            turret = Image.open(config.directory + "//res//vainglory//mapping//turret_grey.png")

        elif color == "blue":  # Open the image for turret color blue
            turret = Image.open(config.directory + "//res//vainglory//mapping//turret_blue.png")

        elif color == "red":  # Open the image for turret color red
            turret = Image.open(config.directory + "//res//vainglory//mapping//turret_red.png")

        else:  # Open the image for turret color grey
            turret = Image.open(config.directory + "//res//vainglory//mapping//turret_grey.png")

        # Scale cords to map size
        x = mapX(cords[0])
        y = mapY(cords[2])

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("TURRET:")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(turret, (x1, y1, x2, y2), turret)

        # Close used img
        turret.close()

        return image

    except Exception as e:
        print("TURRET MARK ERROR:\n" + str(e))


# Add a triangle icon to the given img
def markTriangle(image, cords, color="grey"):
    """
    Mark a triangle icon on a image.
    """

    try:

        # Size of image parts
        sizeX = 11.5
        sixeY = 10

        if color == "grey":  # Open the image for triangle color grey
            triangle = Image.open(config.directory + "//res//vainglory//mapping//triangle_grey.png")

        elif color == "blue":  # Open the image for triangle color blue
            triangle = Image.open(config.directory + "//res//vainglory//mapping//triangle_blue.png")

        elif color == "red":  # Open the image for triangle color red
            triangle = Image.open(config.directory + "//res//vainglory//mapping//triangle_red.png")

        else:  # Open the image for triangle color grey
            triangle = Image.open(config.directory + "//res//vainglory//mapping//triangle_grey.png")

        # Scale cords to map size
        x = mapX(cords[0])
        y = mapY(cords[2])

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("TRIANGLE:")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(triangle, (x1, y1, x2, y2), triangle)

        # Close used img
        triangle.close()

        return image

    except Exception as e:
        print("TRIANGLE MARK ERROR:\n" + str(e))


# Add a shop icon to the given img
def markShop(image, cords, color="grey"):
    """
    Mark a shop icon on a image.
    """

    try:

        # Size of image parts
        sizeX = 14.5
        sixeY = 13.5

        if color == "grey":  # Open the image for shop color grey
            shop = Image.open(config.directory + "//res//vainglory//mapping//shop_grey.png")

        elif color == "blue":  # Open the image for shop color blue
            shop = Image.open(config.directory + "//res//vainglory//mapping//shop_blue.png")

        elif color == "red":  # Open the image for shop color red
            shop = Image.open(config.directory + "//res//vainglory//mapping//shop_red.png")

        else:  # Open the image for shop color grey
            shop = Image.open(config.directory + "//res//vainglory//mapping//shop_grey.png")

        # Scale cords to map size
        x = mapX(cords[0])
        y = mapY(cords[2])

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("SHOP:")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(shop, (x1, y1, x2, y2), shop)

        # Close used img
        shop.close()

        return image

    except Exception as e:
        print("SHOP MARK ERROR:\n" + str(e))


# Add a star icon to the given img
def markStar(image, cords, color="grey"):
    """
    Mark a star icon on a image.
    """

    try:

        # Size of image parts
        sizeX = 16
        sixeY = 16

        if color == "grey":  # Open the image for star color grey
            star = Image.open(config.directory + "//res//vainglory//mapping//star_grey.png")

        elif color == "blue":  # Open the image for star color blue
            star = Image.open(config.directory + "//res//vainglory//mapping//star_blue.png")

        elif color == "red":  # Open the image for star color red
            star = Image.open(config.directory + "//res//vainglory//mapping//star_red.png")

        else:  # Open the image for star color grey
            star = Image.open(config.directory + "//res//vainglory//mapping//star_grey.png")

        # Scale cords to map size
        x = mapX(cords[0])
        y = mapY(cords[2])

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("STAR:")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(star, (x1, y1, x2, y2), star)

        # Close used img
        star.close()

        return image

    except Exception as e:
        print("STAR MARK ERROR:\n" + str(e))


# Add a hero icon to the given img
def markHeroIcon(image, cords, hero="unknown", translateX=0, translateY=0, distance=0, angle=0):
    """
    Mark a hero icon, smaller then profile, on a image.
    """

    try:

        # Size of image parts
        sizeX = 13
        sixeY = 13

        hero = str(tools.cleanHeroName(hero)).lower().replace(" ", "-").replace("_", "-").replace("'", "")

        # Open the hero icon
        try:

            hero = Image.open(config.directory + "//res//vainglory//icons//heros//26x26//" + str(hero) +".png")

        except:
            hero = Image.open(config.directory + "//res//vainglory//icons//heros//26x26//unknown.png")

        # Scale cords to map size
        x = giveX2(mapX(cords[0]), distance, angle) + int(translateX)
        y = giveY2(mapY(cords[2]), distance, angle) + int(translateY)

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("DIMENSIONS: ")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(hero, (x1, y1, x2, y2))

        # Close used img
        hero.close()

        return image

    except Exception as e:
        print("HERO ICON MARK ERROR:\n" + str(e))


# Add a hero icon to the given img
def markHeroProfile(image, cords, realCords=True, hero="unknown", translateX=0, translateY=0, distance=0, angle=0):
    """
    Mark a hero profile pic, bigger then icon, on a image.
    """

    try:

        # Size of image parts
        sizeX = 72
        sixeY = 72

        hero = str(tools.cleanHeroName(hero)).lower().replace(" ", "-").replace("_", "-").replace("'", "")

        # Open the hero icon
        try:

            hero = Image.open(config.directory + "//res//vainglory//icons//heros//" + str(hero) +".png")

        except:
            hero = Image.open(config.directory + "//res//vainglory//icons//heros//unknown.png")

        # Scale cords to map size
        if realCords == False:
            x = giveX2(mapX(cords[0]), distance, angle) + int(translateX)
            y = giveY2(mapY(cords[2]), distance, angle) + int(translateY)

        else:
            x = giveX2(cords[0], distance, angle) + int(translateX)
            y = giveY2(cords[1], distance, angle) + int(translateY)

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("DIMENSIONS: ")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        image.paste(hero, (x1, y1, x2, y2))

        # Close used img
        hero.close()

        return image

    except Exception as e:
        print("HERO PROFILE MARK ERROR:\n" + str(e))


# Add a hero icon to the given img
def markSkillTierProfile(image, cords, realCords=True, skillTier=-1, translateX=0, translateY=0, distance=0, angle=0):
    """
    Mark a skill tier profile pic on a image.
    """

    try:

        # Size of image parts
        sizeX = 72
        sixeY = 72

        skillTier = str(skillTier)

        # Open the hero icon
        try:

            skillTier = Image.open(config.directory + "//res//vainglory//icons//rank//144x144//" + str(skillTier) + ".png")

        except:
            skillTier = Image.open(config.directory + "//res//vainglory//icons//rank//144x144//-1.png")

        # Scale cords to map size
        if realCords == False:
            x = giveX2(mapX(cords[0]), distance, angle) + int(translateX)
            y = giveY2(mapY(cords[2]), distance, angle) + int(translateY)

        else:
            x = giveX2(cords[0], distance, angle) + int(translateX)
            y = giveY2(cords[1], distance, angle) + int(translateY)

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("DIMENSIONS: ")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(skillTier, (x1, y1, x2, y2), skillTier)

        # Close used img
        skillTier.close()

        return image

    except Exception as e:
        print("SKILL TIER PROFILE MARK ERROR:\n" + str(e))


# Mark a hero kill to the given img
def markHeroKill(image, cords, color="grey", hero_1="unknown", hero_2="unknown"):
    """
    Mark a hero kill on a image.
    """

    try:

        # Size of image
        sizeX = 16
        sixeY = 16

        if color == "grey":  # Mark a circle for hero kill
            image = markCircle(image, cords, "grey")

        elif color == "blue":  # Mark a circle for hero kill
            image = markCircle(image, cords, "blue")

        elif color == "red":  # Mark a circle for hero kill
            image = markCircle(image, cords, "red")

        else:  # Mark a circle for hero kill
            image = markCircle(image, cords)

        # Mark the first hero
        image = markHeroIcon(image, cords, hero_1, 0, 17)

        # Mark the second hero
        image = markHeroIcon(image, cords, hero_2, 0, -17)

        return image

    except Exception as e:
        print("HERO KILL MARK ERROR:\n" + str(e))


# Mark a hero kill to the given img
def markHeroAbility(image, cords, ability="unknown", translateX=0, translateY=0, distance=0, angle=0):
    """
    Mark a ability on a image.
    """

    try:

        # Size of image parts
        sizeX = 13
        sixeY = 13

        ability = str(tools.cleanHeroAbility(ability)).lower().replace(" ", "-").replace("_", "-").replace("'", "")

        # Open the hero icon
        try:

            ability = Image.open(config.directory + "//res//vainglory//icons//abilities//26x26//" + str(ability) +".png")

        except:
            ability = Image.open(config.directory + "//res//vainglory//icons//abilities//26x26//unknown.png")

        # Scale cords to map size
        x = giveX2(mapX(cords[0]), distance, angle) + int(translateX)
        y = giveY2(mapY(cords[2]), distance, angle) + int(translateY)

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("DIMENSIONS: ")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(ability, (x1, y1, x2, y2))

        # Close used img
        ability.close()

        return image

    except Exception as e:
        print("ABILITY MARK ERROR:\n" + str(e))


# Mark a hero kill to the given img
def markHeroAbilityUse(image, cords, color="grey", ability="unknown"):
    """
    Mark a hero kill on a image.
    """

    try:

        # Size of image
        sizeX = 16
        sixeY = 16

        if color == "grey":  # Mark a circle for hero kill
            image = markStar(image, cords, "grey")

        elif color == "blue":  # Mark a circle for hero kill
            image = markStar(image, cords, "blue")

        elif color == "red":  # Mark a circle for hero kill
            image = markStar(image, cords, "red")

        else:  # Mark a circle for hero kill
            image = markStar(image, cords)

        # Mark the hero ability
        image = markHeroAbility(image, cords, ability, 0, 17)

        return image

    except Exception as e:
        print("ABILITY USE MARK ERROR:\n" + str(e))


# Mark a hero kill to the given img
def markItem(image, cords, item="unknown", translateX=0, translateY=0, distance=0, angle=0):
    """
    Mark a item on a image.
    """

    try:

        # Size of image parts
        sizeX = 13
        sixeY = 13

        item = str(tools.cleanItemName(item)).lower().replace(" ", "-").replace("_", "-").replace("'", "")

        # Open the hero icon
        try:

            item = Image.open(config.directory + "//res//vainglory//icons//items//26x26//" + str(item) + ".png")

        except:
            item = Image.open(config.directory + "//res//vainglory//icons//items//26x26//unknown.png")

        # Scale cords to map size
        x = giveX2(mapX(cords[0]), distance, angle) + int(translateX)
        y = giveY2(mapY(cords[2]), distance, angle) + int(translateY)

        # Top left corner cords
        x1 = int(x - sizeX)
        y1 = int(y - sixeY)
        # Bottom right corner cords
        x2 = int(x + sizeX)
        y2 = int(y + sixeY)

        # FOR DEBUGGING
        # print("DIMENSIONS: ")
        # print("X1: " + str(x1) + " |Y1: " + str(y1) + " |X2: " + str(x2) + " |Y2: " + str(y2))
        # print("X Scale: " + str(x2 - x1) + " |Y Scale: " + str(y2 - y1))

        # kraken.show()
        image.paste(item, (x1, y1, x2, y2))

        # Close used img
        item.close()

        return image

    except Exception as e:
        print("ABILITY MARK ERROR:\n" + str(e))


# Mark a hero kill to the given img
def markItemAbilityUse(image, cords, color="grey", item="unknown"):
    """
    Mark a hero kill on a image.
    """

    try:

        # Size of image
        sizeX = 16
        sixeY = 16

        if color == "grey":  # Mark a circle for hero kill
            image = markTriangle(image, cords, "grey")

        elif color == "blue":  # Mark a circle for hero kill
            image = markTriangle(image, cords, "blue")

        elif color == "red":  # Mark a circle for hero kill
            image = markTriangle(image, cords, "red")

        else:  # Mark a circle for hero kill
            image = markTriangle(image, cords)

        # Mark the hero ability
        image = markItem(image, cords, item, 0, 17)

        return image

    except Exception as e:
        print("ABILITY USE MARK ERROR:\n" + str(e))


# Mark a hero kill to the given img
def markItemBuy(image, cords, color="grey", item="unknown"):
    """
    Mark a hero kill on a image.
    """

    try:

        # Size of image
        sizeX = 16
        sixeY = 16

        if color == "grey":  # Mark a circle for hero kill
            image = markShop(image, cords, "grey")

        elif color == "blue":  # Mark a circle for hero kill
            image = markShop(image, cords, "blue")

        elif color == "red":  # Mark a circle for hero kill
            image = markShop(image, cords, "red")

        else:  # Mark a circle for hero kill
            image = markShop(image, cords)

        # Mark the hero ability
        image = markItem(image, cords, item, 0, 0, 17, random.randrange(0, 361))

        return image

    except Exception as e:
        print("ABILITY USE MARK ERROR:\n" + str(e))


def generateGIF(matchData, ign, mode=5, randomID=random.randrange(1, 9999999999)):
    """Creates a gif out of a Vainglory match telemetry.

    :param matchData: Matches data.
    :param ign: Players IGN.
    :param mode: What sorta data should be marked.
    :param randomID: ID of gif in local memory.
    :returns: Path to the GIF.

    """

    try:

        startImage = Image.open(config.directory + "//res//vainglory//mapping//start.png")

        fontType = ImageFont.truetype(config.directory + "//res//fonts//arial.ttf", 100)
        drawImage = ImageDraw.Draw(startImage)

        num = 0
        mainSide = "Right"
        enemySide = "Left"
        participantNum = random.randint(0, 6)
        for roster in matchData["rosters"]:
            for participant in roster["participants"]:
                if ign != "$random$":
                    if participant["player"]["name"] == ign:
                        mainActor = tools.cleanHeroName(participant["actor"])
                        if "right" in roster["side"]:
                            mainSide = "Right"
                            enemySide = "Left"

                        else:
                            mainSide = "Left"
                            enemySide = "Right"

                        break  # We have what we want so break

                else:
                    if num == participantNum:
                        mainActor = tools.cleanHeroName(participant["actor"])
                        if "right" in roster["side"]:
                            mainSide = "Right"
                            enemySide = "Left"

                        else:
                            mainSide = "Left"
                            enemySide = "Right"

                        break  # We have what we want so break

                num += 1

        # Draw on start of gif match information
        w, h = drawImage.textsize(text="ID:\n" + str(matchData["id"]), font=fontType)
        drawImage.text(xy=((1234 - (w / 2)), 45), text="Match ID:\n" + str(matchData["id"]), fill=(195, 66, 255), font=fontType, align="center")  # Match ID
        for roster in matchData["rosters"]:

            if str(mainSide).lower() in roster["side"]:
                rgb = (20, 186, 224)  # Player side

            else:
                rgb = (230, 70, 11)  # Enemy side

            if "left" in roster["side"]:
                x = 120

            else:
                x = 1570

            y = 200

            for participant in roster["participants"]:

                y += 150

                difference = list(drawImage.textsize(text=participant["player"]["name"], font=fontType))[0]
                drawImage.text(xy=(x, y), text=participant["player"]["name"], fill=rgb, font=fontType)

                # FOR DEBUGGING
                # print("DIFFERENCE: " + str(difference))
                # print("ACTOR: " + str(participant["actor"]))
                # print("SKILL TIER: " + str(participant["skillTier"]))

                markHeroProfile(image=startImage, cords=[x, y], realCords=True, hero=str(participant["actor"]), translateX=int(difference + 82), translateY=62)
                markSkillTierProfile(image=startImage, cords=[x, y], realCords=True, skillTier=int(participant["skillTier"]), translateX=-62, translateY=62)

        # RESIZE IMAGE
        size = 1000, 1000
        startImage.thumbnail(size, Image.ANTIALIAS)

        # FOR DEBUGGING
        # startImage.save(config.directory + "//temp//" + str(random.randrange(1, 9999999999)) + ".png")

        data = tools.matchTimeLine(matchData, ign)

        # List of images
        images = []
        for minute in data:
            # Start with a fresh map
            image = Image.open(config.directory + "//res//vainglory//mapping//bot_map.png")

            for event in data[minute]:
                # What Team does this event belongs to
                if event["payload"]["Team"] == mainSide:
                    color = "blue"

                elif event["payload"]["Team"] == enemySide:
                    color = "red"

                else:
                    color = "grey"

                if event["type"] == "KillActor" and mode in [1, 5]:
                    # Get cords
                    cords = event["payload"]["Position"]

                    # If it's a hero kill mark hero kill
                    if event["payload"]["TargetIsHero"] == 1:
                        # Get the killer hero
                        hero_1 = event["payload"]["Actor"]

                        # Get the hero killed
                        hero_2 = event["payload"]["Killed"]

                        # FOR DEBUGGING
                        # print("KILLER:   " + str(hero_1) + " |KILLED:   " + str(hero_2))

                        # Mark hero kill for hero kill
                        markHeroKill(image, cords, color, hero_1, hero_2)

                    # If it's a turret mark a turret
                    elif event["payload"]["Killed"] in ["*Turret*", "*VainTurret*"]:
                        # Mark turret
                        image = markTurret(image, cords, color)

                    # If it's a gold or crystal miner mark a flag
                    elif event["payload"]["Killed"] in ["*JungleMinion_GoldMiner*", "*JungleMinion_CrystalMiner*"]:
                        # Mark flag
                        image = markFlag(image, cords, color)

                    # If it's a kraken mark a kraken
                    elif event["payload"]["Killed"] in ["*Kraken_Captured*", "*Kraken_Jungle*"]:
                        # Mark kraken capture
                        image = markKraken(image, cords, color)

                    # If it's a vain crystal mark a crystal
                    elif event["payload"]["Killed"] in ["*VainCrystalAway*", "*VainCrystalHome*"]:
                        # Mark crystal
                        image = markCrystal(image, cords, color)

                    # If it's nothing above mark a dot
                    else:
                        # Mark dot
                        image = markDot(image, cords, color)

                elif event["type"] == "UseAbility" and mode in [3, 5]:
                    # Get cords
                    cords = event["payload"]["Position"]

                    ability = event["payload"]["Ability"]

                    markHeroAbilityUse(image, cords, color, ability)

                elif event["type"] == "UseItemAbility" and mode in [4, 5]:
                    # Get cords
                    cords = event["payload"]["Position"]

                    ability = event["payload"]["Ability"]

                    markItemAbilityUse(image, cords, color, ability)

                elif event["type"] == "BuyItem" and mode in [5]:
                    # Get cords
                    cords = event["payload"]["Position"]

                    item = event["payload"]["Item"]

                    markItemBuy(image, cords, color, item)

                elif event["type"] == "NPCkillNPC" and mode in [2, 5]:
                    # Get cords
                    cords = event["payload"]["Position"]

                    # If it's a hero mark circle
                    if event["payload"]["TargetIsHero"] == 1:

                        # Get the killer hero
                        hero_1 = event["payload"]["Actor"]

                        # Get the hero killed
                        hero_2 = event["payload"]["Killed"]

                        # FOR DEBUGGING
                        # print("KILLER:   " + str(hero_1) + " |KILLED:   " + str(hero_2))

                        # Mark hero kill for hero kill
                        markHeroKill(image, cords, color, hero_1, hero_2)

                    # If it's a turret mark a turret
                    elif event["payload"]["Killed"] in ["*Turret*", "*VainTurret*"]:
                        # Mark turret
                        image = markTurret(image, cords, color)

                    # If it's a gold or crystal miner mark a flag
                    elif event["payload"]["Killed"] in ["*JungleMinion_GoldMiner*", "*JungleMinion_CrystalMiner*"]:
                        # Mark flag
                        image = markFlag(image, cords, color)

                    # If it's a kraken mark a kraken
                    elif event["payload"]["Killed"] in ["*Kraken_Captured*", "*Kraken_Jungle*"]:
                        # Mark kraken capture
                        image = markKraken(image, cords, color)

                    # If it's a vain crystal mark a crystal
                    elif event["payload"]["Killed"] in ["*VainCrystalAway*", "*VainCrystalHome*"]:
                        # Mark crystal
                        image = markCrystal(image, cords, color)

                    # If it's nothing above mark a dot
                    else:
                        # Mark dot
                        image = markDot(image, cords, color)

                elif event["type"] == "Executed" and mode in [4, 5]:
                    # Get cords
                    cords = event["payload"]["Position"]

                    # If it's a hero mark circle
                    if event["payload"]["TargetIsHero"] == 1:

                        # Get the killer hero
                        hero_1 = event["payload"]["Actor"]

                        # Get the hero killed
                        hero_2 = event["payload"]["Killed"]

                        # FOR DEBUGGING
                        # print("KILLER:   " + str(hero_1) + " |KILLED:   " + str(hero_2))

                        # Mark hero kill for hero kill
                        markHeroKill(image, cords, color, hero_1, hero_2)

                    # If it's a turret mark a turret
                    elif event["payload"]["Killed"] in ["*Turret*", "*VainTurret*"]:
                        # Mark turret
                        image = markTurret(image, cords, color)

                    # If it's a gold or crystal miner mark a flag
                    elif event["payload"]["Killed"] in ["*JungleMinion_GoldMiner*", "*JungleMinion_CrystalMiner*"]:
                        # Mark flag
                        image = markFlag(image, cords, color)

                    # If it's a kraken mark a kraken
                    elif event["payload"]["Killed"] in ["*Kraken_Captured*", "*Kraken_Jungle*"]:
                        # Mark kraken capture
                        image = markKraken(image, cords, color)

                    # If it's a vain crystal mark a crystal
                    elif event["payload"]["Killed"] in ["*VainCrystalAway*", "*VainCrystalHome*"]:
                        # Mark crystal
                        image = markCrystal(image, cords, color)

                    # If it's nothing above mark a dot
                    else:
                        # Mark dot
                        image = markDot(image, cords, color)

            # RESIZE IMAGE
            size = 1000, 1000
            image.thumbnail(size, Image.ANTIALIAS)

            images.append(image)
            # FOR DEBUGGING
            # image.save(config.directory + "//temp//" + str(random.randrange(1, 9999999999)) + ".png")

        # FOR DEBUGGING
        # print("IMAGES: " + str(images))

        path = config.directory + "//temp//" + str(randomID) + ".gif"

        #  FOR DEBUGGING
        # print("GIF PATH:   " + str(path))

        startImage.save(path, save_all=True, append_images=images, duration=1000, loop=10)

        # Close everything up
        startImage.close()
        for subImage in images:
            subImage.close()

        return path  # Return the path to the gif

    except Exception as e:
        print("GIF ERROR:   " + str(e) + "\n" + str(traceback.format_exc()))
