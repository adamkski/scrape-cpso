library(tidyverse)
library(here)

city_lastname <- read_csv(here("data-doctors/dr-Perth-lastname.csv"))
city <- read_csv(here("data-doctors/dr-Perth-full.csv"))

city_lastname %>% 
  summarise( n = n_distinct(CPSO_num))
city %>% 
  summarise( n = n_distinct(CPSO_num))
