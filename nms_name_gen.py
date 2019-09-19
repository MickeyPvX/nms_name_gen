import click

from googletrans import Translator
from utils.star_class_map import spectral_class_map, oddity_map
from utils.translation_tools import engrishify
from app.portmanfaux import PortManFaux
from app.star_class import StarClass


@click.group()
def main():
    """
    It's a start!
    """


@click.command()
@click.argument('word')
def translate(word):
    """
    This command translates an English input word to Icelandic and outputs it to the console

    :param word (str): input word in English
    :return:
    """
    trans = Translator(service_urls=['translate.google.com'])
    icelandic = trans.translate(word, src='en', dest='is').text.lower()
    display_word = engrishify(icelandic)
    click.echo(f'{word} -> {display_word}')

    return


@click.command()
@click.option('--min-len', '-m', help='Minimum length of words to generate', type=int)
@click.option('--number', '-n', help='Number of words to generate', type=int)
@click.argument('input_words')
def portmanfaux(**kwargs):
    """
    Generates a list of portman-faux words from input words and outputs them to the console

    :param min_len (int): minimum length of the words to return
    :param number (int): number of words to generate
    :param input_words (str): words to use separated by commas
    :return:
    """
    word_list = kwargs.pop('input_words').split(',')

    click.echo(f'Words used: {word_list}')

    prospect_args = {key: value for key, value in kwargs.items() if value is not None}

    word_gen = PortManFaux(input_words=word_list)
    prospects = word_gen.get_prospects(**prospect_args)

    for prospect in prospects:
        click.echo(prospect)

    return


@click.command()
@click.option('--min-len', '-m', help='Minimum length of names to generate', type=int)
@click.option('--number', '-n', help='Number of names to generate', type=int)
@click.argument('spectral_class')
@click.argument('region')
def name_star(**kwargs):
    """
    Based on an input spectral class and region, generates prospective star names and outputs them to the console

    :param spectral_class (str): the NMS spectral class e.g. "F0", "B3ef", "O9v", etc.
    :param region (str): the NMS region where the star resides
    :param number (int): number of prospective star names to generate
    :param min_len (int): minimun length of the star names to generate
    :return:
    """
    spectral_class = kwargs.pop('spectral_class')
    name_args = {key: value for key, value in kwargs.items() if value is not None}

    star_name_gen = StarClass(spectral_class)
    star_prospects = star_name_gen.generate_names(**name_args)

    click.echo(
        (
            f'\nStar Class: {star_name_gen.spectral_class_str}\n'
            f'Deity Root: {star_name_gen.deity}\n'
            f'Region: {kwargs["region"].title()}\n'
        )
    )

    for prospect in star_prospects:
        click.echo(prospect)

    return


def entrypoint():
    main.add_command(translate)
    main.add_command(portmanfaux)
    main.add_command(name_star)
    main()
