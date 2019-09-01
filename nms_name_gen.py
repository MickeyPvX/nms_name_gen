import click

from googletrans import Translator
from utils.star_class_map import spectral_class_map, oddity_map
from utils.portmanfaux import PortManFaux


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
    trans = Translator()
    icelandic = trans.translate(word, dest='is').text
    click.echo(f'{word} -> {icelandic}')

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

    prospect_args = {
        key: value
        for key, value in kwargs.items()
        if value is not None
    }

    word_gen = PortManFaux(input_words=word_list)
    prospects = word_gen.get_prospects(**prospect_args)

    for prospect in prospects:
        click.echo(prospect)

    return


def entrypoint():
    main.add_command(translate)
    main.add_command(portmanfaux)
    main()
