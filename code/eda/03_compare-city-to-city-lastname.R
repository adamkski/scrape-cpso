library(tidyverse)
library(stringr)
library(here)

city_codes <- read_csv(here("data/city_codes.csv"))
cities <- read_csv(here("data/count-doc-by-city.csv"))
cities <- cities %>% 
  left_join( city_codes, by = "city_code")

# use fsa search
file_list <- fs::dir_ls( here("data-doctors/"), regex = "\\w\\d\\w")
fsa <- map(file_list, read_csv) %>% 
  bind_rows()

fsa %>% 
  separate( city_name, into = c('fsa_col', 'city')) %>% 
  mutate( city_name = str_c( toupper(str_sub( city, 1, 1 )), str_sub( city, 2 ) )) %>% 
  group_by(city_name) %>% 
  summarise( scraped = n_distinct(CPSO_num)) %>% 
  left_join( cities %>% select(-city_code) %>% rename( expected = num_doctors), by = "city_name") %>% 
  mutate( p = round(scraped / expected, 2) )


# use city-lastname search
file_list <- fs::dir_ls( here("data-doctors/"), regex = "lastname")
city_lastname <- map(file_list, read_csv) %>% 
  bind_rows()

city_lastname %>% 
  group_by(city_name) %>% 
  summarise( scraped = n_distinct(CPSO_num)) %>% 
  left_join( cities %>% select(-city_code) %>% rename( expected = num_doctors), by = "city_name") %>% 
  mutate( p = round(scraped / expected, 2) )
