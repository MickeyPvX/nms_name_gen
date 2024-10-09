# No Man's Sky Name Generator

| ![Python Version](https://img.shields.io/badge/Python-3.12-blue) | ![Interrogate Coverage](./.github/badges/interrogate_badge.svg) |

## Overview

* This naming generator for No Man's Sky adhere's to Odin's naming convention for stars and planets:
  * [OdinGaming Naming Convention](https://www.odingaming.com/2018/01/15/no-mans-sky-naming-convention)

* [x] Basic maps for star classes and oddities
* [x] Portmanfaux generator
* [x] Basic word translation to Icelandic
* [x] Star naming
* [x] Planet naming

## Installation

nms_name_gen uses the Click package with poetry integration to generate a command line interface:

* [Poetry](https://python-poetry.org/docs/)

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
