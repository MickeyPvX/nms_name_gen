# No Man's Sky Name Generator

![Python Version](https://img.shields.io/badge/Python-3.12-blue) ![Interrogate Coverage](./.github/badges/interrogate_badge.svg)

## Overview

Unfortunately, the webpage with the original naming strategy for this app has been taken down, so here's what this actually does:

* Star Naming
  * For naming stars, you only need the spectral class string and the region in which the star resides, e.g. `F0P`, `B4K`, etc.  Check [star_class_map.py](./src/utils/star_class_map.py) for all available spectral classes and oddity types.
  * The star name generator maps the spectral class to a deity name, then smashes that word together with the name of the region, and adds the oddity types as a prefix or suffix, depending on if there is more than one (but no more than 2).  It then gives you `n` options on what you can name your star.
  * Example
    * Spectral Class: `F0PH`
    * Region: `Somewhere`
    * Potential name generated: `Op-Khohere-Ah`

* Planet Naming
  * Naming planets requires a few more inputs that are in the planet's details, including Sentinal Activity, Weather, Flora, and Fauna density.  You'll also need to know the name of the star of the system it's in.
  * The planet name generator does the same portman-faux as the star name generator, only this time it joins the star name and the planet's weather, translated to Icelandic (why?  I dunno, that's how the naming strategy I built this from did...and it added an interesting challenge from a programming standpoint).  Extreme planets are prefixed with `Ex-`.  The suffix is the hard part: the Sentinal activity, flora, and fauna are all translated to Icelandic, the first syllable of each is extracted, and joined together.
  * Example:
    * Star Name: `Khohere` (just use the root star name without the oddity prefix/suffix)
    * Weather: `Balmy`
    * Sentinals: `Aggressive`
    * Flora: `Bountiful`
    * Fauna: `Abundant`
    * Potential name generated: `Sleaohere-Ownaegnohg`

## Installation

nms_name_gen uses the Click package with poetry integration to generate a command line interface:

* [Poetry](https://python-poetry.org/docs/)

1. Create a new virtual environment, I like to create it in the repo's root directory using `virtualenv`
    * `virtualenv -p=python3.12 venv && source venv/bin/activate`

2. Install the app
    * `poetry install`

3. Run it!  You can either run it through poetry or the CLI should be installed in your virtual environment:
    * `poetry run nms-name-gen [COMMAND] [ARGS]`
    * `nms-name-gen [COMMAND] [ARGS]`

## Setup

nms_name_gen currently uses Microsoft Azure Translator Text API:

* [Translator Text API](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/reference/v3-0-reference)

Once you have that set up, copy the nms_config.example.json file and rename it nms_config.json.  Replace the translate_url and translate_key values with your values.

## Usage

### Available Commands

* `translate` - translates a word or phrase to Icelandic
* `portmanfaux` - blends two words together; does not take into account their meanings
* `name-star` - outputs prospective star names based on user input
* `name-planet` - outputs prospective planet names based on user input
