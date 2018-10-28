from cpso import *
import winsound

#cities = { "2067": "Windsor" }
cities = { "1739": "Perth" }

start_time = time.time()

for city_code, city in cities.items():
    one_city = {}

    for char_1 in ascii_lowercase:
        char = char_1

        try:
            n_dr = count_doctors( city_code, '', char )
            print( f"{city}-{char}: found {n_dr}")

        except:
            print( f"{city}-{char}: none found")
            continue

        # if n results for one letter are below threshold, stop
        if n_dr < 1000:
            one_city.update( crawl_cpso( city_code, '', char ) )
            continue

        # otherwise move to two letters
        for char_2 in ascii_lowercase:
            char = char_1 + char_2

            try:
                n_dr = count_doctors( city_code, '', char )
                print( f"{city}-{char}: found {n_dr}")
                one_city.update( crawl_cpso( city_code, '', char ) )
            except:
                print( f"{city}-{char}: none found")
                continue

    with open( f'{project_dir}/data-raw/dr-{city}-lastname.csv', 'w' ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow( ['city_name', 'CPSO', 'article'] )
        for key, val in one_city.items():
            writer.writerow( [city, key, val] )

winsound.MessageBeep()
elapsed_time = time.time() - start_time
print(time.strftime("-- time elapsed for scrape: %H:%M:%S -- ", time.gmtime(elapsed_time)))
