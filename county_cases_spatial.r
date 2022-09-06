library(tidyverse)
library(tmap)
library(sf)
library(sp)

county_shape = st_read("county_cases.csv", package = "sf")
county_cases = county_shape[ , c("cases", "County")]
kenya_shp =read_sf("kenyan-counties/County.shp")
kenya_shp$COUNTY[kenya_shp$COUNTY == "Tharaka" ]<- "Tharaka Nithi"
kenya_shp$COUNTY[kenya_shp$COUNTY == "Keiyo-Marakwet" ]<- "Elgeyo Marakwet"
names(kenya_shp)[names(kenya_shp) == "COUNTY"] <- "County"
kenya_covid_cases = merge(kenya_shp, county_cases, all = TRUE, by=c("County"))
kenya_covid_cases$cases = as.numeric(kenya_covid_cases$cases)


png("plot_county_cases.png")
tmap_mode("view")
tm_shape(kenya_covid_cases)+
  #tm_polygons(col = "cases",style="quantile", palette = "Oranges", contrast=1,border.col = "black",
  #            border.alpha = 0.08, title = "Cases", breaks = c(0,1000, 10000))+#, breaks=c(0,1000))+
  tm_fill("cases",palette = "Reds", style = "quantile")+
  tm_borders(alpha=0.08)+
  tmap_options(max.categories = 47, bg.color = "white")+
  tm_layout(frame=FALSE, legend.position = c("left","bottom"))+
  tm_compass(position = c(0.9,0.1), text.size=0.5, size=2)

dev.off()
