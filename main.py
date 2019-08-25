from utils.star_class_map import spectral_class_map, oddity_map

test_string = 'O4pq'

chopped_string = list(test_string)

spectral_class = chopped_string[0]
brightness = int(chopped_string[1]) // 2
oddities = []

if len(chopped_string) > 2:
    oddities = [oddity_map[oddity.upper()] for oddity in chopped_string[2:]]

print(spectral_class_map[spectral_class][brightness], oddities)
