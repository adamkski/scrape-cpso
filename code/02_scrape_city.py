from cpso import *
import winsound

#cities = { "2067": "Windsor" }
cities = { "1739": "Perth" }

start_time = time.time()

for city_code, city in cities.items():
    one_city = {}

    one_city.update( crawl_cpso( city_code ) )

    with open( f'{project_dir}/data-raw/dr-{city}-city.csv', 'w' ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow( ['city_name', 'CPSO', 'article'] )
        for key, val in one_city.items():
            writer.writerow( [city, key, val] )

winsound.MessageBeep()
elapsed_time = time.time() - start_time
print(time.strftime("-- time elapsed for scrape: %H:%M:%S -- ", time.gmtime(elapsed_time)))
