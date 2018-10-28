#' we want to know if the number of doctors scraped matches
#' the number of search results found

library(tidyverse)
library(here)

# load doctors we scraped
file_list <- fs::dir_ls( here("data-doctors"))
scraped_doctors <- map(file_list, read_csv) %>%
  bind_rows

# load driver files for fsa scrape
file_list <- fs::dir_ls( here("data"), regexp = "count-doc_fsa" ) 
count_by_fsa <- map( file_list, read_csv ) %>% 
  bind_rows

# load driver files for city count
count_by_city <- read_csv( here("data/count-doc-by-city.csv") )
city_codes <- read_csv( here("data/city_codes.csv") )
count_by_city <- count_by_city %>% 
  left_join( city_codes, by = "city_code" )

# check if it equals a blank general search (42,779)
sum(count_by_city$num_doctors)
# it's already bigger... because of double counting 

# check the big ones
count_by_city %>% 
  filter( city_name %in% c('Brampton', 'Hamilton', 'London', 'Mississauga', 'Ottawa', 'Toronto'))



# compare distinct CPSO numbers scraped to search result count
# by city
scraped_doctors %>% 
  group_by( city_name ) %>% 
  summarise( scraped = n_distinct(CPSO_num)) %>% 
  full_join( counts_doctors %>% 
               group_by( city_name ) %>% 
               summarise( expected = sum( num_doctors, na.rm = T )), by = "city_name" ) %>% 
  mutate( p = round(scraped / expected, 2) )

# why do we have *more* scraped than expected for toronto
# try looking at fsa
scraped_doctors %>% 
  group_by( city_name, fsa ) %>% 
  summarise( scraped = n_distinct(CPSO_num)) %>% 
  full_join( counts_doctors %>% select( fsa, expected = num_doctors ), by = "fsa" ) %>% 
  mutate( p = round(scraped / expected, 2) ) 
# can't find any over/under?