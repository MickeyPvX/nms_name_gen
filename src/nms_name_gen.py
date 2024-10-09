"""NMS Name Generator main interface"""

import json
from os import path

import click

from config import NMSConfig
from planet_name import PlanetName
from pmf_gen import PortManFaux
from star_class import StarClass
from utils.translation_tools import map_or_translate

SORT_MAP = {"ASC": False, "DESC": True}

config = NMSConfig()
translation_map = json.load(
    open(file=path.join(f"{path.dirname(__file__)}", "app", "translation_map.json"), encoding="utf-8")
)


@click.group()
def main():
    """
    It's a start!
    """


@main.command()
@click.option("-w", "--words", type=click.STRING, multiple=True)
def translate(words):
    """
    This command translates an English input word to Icelandic and outputs it to the console

    :param word (str): input word in English
    :return:
    """
    translation = map_or_translate(words, translation_map, config.translator)

    for word, icelandic in translation.items():
        click.echo(f"{word} -> {icelandic}")

    return


@main.command()
@click.option("--min-len", "-m", help="Minimum length of words to generate", type=int)
@click.option("--number", "-n", help="Number of words to generate", type=int)
@click.argument("word_1")
@click.argument("word_2")
def portmanfaux(word_1, word_2, **kwargs):
    """
    Generates a list of portman-faux words from input words and outputs them to the console

    :param min_len (int): minimum length of the words to return
    :param number (int): number of words to generate
    :param word_1 (str): first word to blend
    :param word_2 (str): second word to blend
    :return:
    """
    word_list = [word_1, word_2]

    click.echo(f"Words used: {word_list}")

    prospect_args = {key: value for key, value in kwargs.items() if value is not None}

    word_gen = PortManFaux(input_words=word_list)
    prospects = word_gen.get_prospects(**prospect_args)

    for prospect in prospects:
        click.echo(prospect)

    return


@main.command()
@click.option("--min-len", "-m", help="Minimum length of names to generate", type=click.INT)
@click.option("--number", "-n", help="Number of names to generate", type=click.INT)
@click.option("--sort", "-s", type=click.Choice(["ASC", "DESC"]))
@click.argument("spectral_class")
@click.argument("region")
def name_star(**kwargs):
    """
    Based on an input spectral class and region, generates prospective star names and outputs them to the console

    :param spectral_class (str): the NMS spectral class e.g. "F0", "B3ef", "O9v", etc.
    :param region (str): the NMS region where the star resides
    :param number (int): number of prospective star names to generate
    :param min_len (int): minimun length of the star names to generate
    :return:
    """
    spectral_class = kwargs.pop("spectral_class")
    sort_dir = kwargs.pop("sort", False)

    name_args = {key: value for key, value in kwargs.items() if value is not None}

    star_name_gen = StarClass(spectral_class)
    star_prospects = star_name_gen.generate_names(**name_args)

    click.echo(
        (
            f"\nStar Class: {star_name_gen.spectral_class_str}\n"
            f"Deity Root: {star_name_gen.deity}\n"
            f'Region: {kwargs["region"].title()}\n'
        )
    )

    for prospect in sorted(star_prospects, reverse=SORT_MAP.get(sort_dir, False)):
        click.echo(prospect)

    return


@main.command()
@click.option("--min-len", "-m", help="Minimum length of names to generate", type=int)
@click.option("--number", "-n", help="Number of names to generate", type=int)
@click.option("--sort", "-s", type=click.Choice(["ASC", "DESC"]))
@click.option("--extreme", "-x", is_flag=True)
@click.option("--star_name", "-sn", prompt=True)
@click.option("--weather", "-w", prompt=True)
@click.option("--sentinals", "-sl", prompt=True)
@click.option("--flora", "-fl", prompt=True)
@click.option("--fauna", "-fa", prompt=True)
def name_planet(**kwargs):
    """
    Based on the name of the star of the planet's solar system, the planet's weather, flora, and fauna,
    generates prospective planet names and outputs them to the console.

    :param star_name (str): name of the star of the planet's solar system
    :param weather (str): the planet's weather; if two words, use one of them
    :param sentinals (str): the planet's sentinal behavior
    :param flora (str): the planet's flora density
    :param fauna (str): the planet's fauna density
    :return:
    """
    sort_dir = kwargs.pop("sort", False)
    name_args = {key: kwargs.pop(key) for key in ["min_len", "number", "extreme"] if kwargs.get(key) is not None}

    namer = PlanetName(**kwargs)
    planet_prospects = namer.generate_names(**name_args)

    for prospect in sorted(planet_prospects, reverse=SORT_MAP.get(sort_dir, False)):
        click.echo(prospect)

    return
