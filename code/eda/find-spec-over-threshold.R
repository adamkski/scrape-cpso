library(tidyverse)

# count specialists
spec <- bind_rows(
  read_csv("C:/Users/adamn/projects/scrape-cpso/data/count-spec_London.csv"),
  read_csv("C:/Users/adamn/projects/scrape-cpso/data/count-spec_Brampton.csv"),
  read_csv("C:/Users/adamn/projects/scrape-cpso/data/count-spec_Hamilton.csv"),
  read_csv("C:/Users/adamn/projects/scrape-cpso/data/count-spec_Mississauga.csv"),
  read_csv("C:/Users/adamn/projects/scrape-cpso/data/count-spec_Ottawa.csv"),
  read_csv("C:/Users/adamn/projects/scrape-cpso/data/count-spec_Toronto.csv")  
)
spec %>% 
  filter( num_doctors > 1000 )

spec %>% 
  ggplot( aes(num_doctors) ) + 
  geom_histogram()


# count all doctors
all_doc <- read_csv("C:/Users/adamn/projects/scrape-cpso/data/count-doc-by-city.csv")
city_codes <- read_csv( "C:/Users/adamn/projects/scrape-cpso/data/city_codes.csv" )

# add city name
all_doc <- all_doc %>% 
  left_join( city_codes, by = "city_code")

# sum up specialists
total_spec <- spec %>% 
  group_by( city_code ) %>% 
  summarise( total_spec = sum(num_doctors) )

# compare totals (there appear to be doctors with multiple specializations, not perfect)
all_doc %>% 
  left_join( total_spec, by = "city_code" ) %>% 
  mutate( family_docs = num_doctors - total_spec )


# validate count of doctors from postal codes

