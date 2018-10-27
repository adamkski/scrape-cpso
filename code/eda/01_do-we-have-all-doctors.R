#' we want to know if the number of doctors scraped matches
#' the number of search results found

library(tidyverse)
library(here)

# load doctors we scraped
file_list <- fs::dir_ls( here("data-doctors"))
scraped_doctors <- map(file_list, read_csv) %>%
  bind_rows

# load driver files for scrape
file_list <- fs::dir_ls( here("data"), regexp = "count-doc_fsa" ) 
counts_doctors <- map( file_list, read_csv ) %>% 
  bind_rows

# summarize
scraped_doctors %>% 
  count( city_name ) %>% 
  rename( scraped = n ) %>% 
  full_join( counts_doctors %>% 
               group_by( city_name ) %>% 
               summarise( expected = sum( num_doctors, na.rm = T )), by = "city_name" ) %>% 
  mutate( p = round(scraped / expected, 2) )

# note there's 42,780 doctors in the CPSO database if advanced search
# is made using defaults and no entered options

