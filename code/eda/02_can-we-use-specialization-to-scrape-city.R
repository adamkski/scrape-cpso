library(tidyverse)
library(here)

# we'll try to split postal code into specializations
# e.g. M5G

m5g <- read_csv( here("data/count-doc_spec_fsa-M5G.csv") )

# need to make sure that family doctors + doctors with specialty
# equals total doctors for an FSA

# first, will this work, are all spec sub 1000
m5g %>% 
  filter( num_doctors > 1000 )
# check

m5g %>% 
  write.table("clipboard", sep="\t", row.names=FALSE)

# we're still missing 878 doctors from the total count...
# that does get us much closer though...