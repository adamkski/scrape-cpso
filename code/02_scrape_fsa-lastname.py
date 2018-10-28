from cpso import *


"""# scrape an fsa by first letter of last name
city = "fsa_toronto"
fsas = [ 'K1H', 'M5T', 'N6A']
for fsa in fsas:
    one_fsa = {}
    # progress bar settings
    total = 26
    k = 0
    start_time = time.time()

    for char in ascii_lowercase:
        progress(k, total, status= 'scraping ' + fsa + ' ' + char )

        try:
            one_fsa.update( crawl_fsa( fsa, char ) )
        except:
            pass
        finally:
            k += 1

    with open( project_dir + '/data-raw/doctors-' + fsa + '.csv', 'w' ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow( ['city_name', 'fsa', 'CPSO', 'article'] )
        for key, val in one_fsa.items():
            writer.writerow( [city, fsa, key, val] )

    k = total
    progress(k, total, status= 'finished ' + fsa )
    print()
    elapsed_time = time.time() - start_time
    print(time.strftime("-- time elapsed for scrape: %H:%M:%S -- ", time.gmtime(elapsed_time)))
"""


"""# scrape big cities by fsa
#cities = ['fsa_brampton', 'fsa_hamilton', 'fsa_london', 'fsa_mississauga', 'fsa_ottawa', 'fsa_toronto']
cities = [ 'fsa_hamilton', 'fsa_london', 'fsa_ottawa', 'fsa_toronto']
start_time = time.time()

for j, city in enumerate(cities):

    print()
    print( city, j+1, "of", len(cities) )

    with open( project_dir + '/data/' + city + '.pickle', 'rb') as f:
        fsas = pickle.load(f)

    # progress bar settings
    total = len(fsas) - 1
    k = 0

    for fsa in fsas:
        doctors = {}
        progress(k, total, status= 'scraping ' + fsa )

        with open( project_dir + '/data-raw/doctors-' + fsa + '.csv', 'w' ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow( ['city_name', 'fsa', 'CPSO', 'article'] )

            try:
                crawl_fsa( fsa )
                for key, val in doctors.items():
                    writer.writerow( [city, fsa, key, val] )
            except:
                #print( "no doctors in", fsa )
                writer.writerow( [city, fsa, "NA", "NA"] )

            finally:
                k += 1

elapsed_time = time.time() - start_time
print(time.strftime("-- time elapsed for scrape: %H:%M:%S -- ", time.gmtime(elapsed_time)))
"""
