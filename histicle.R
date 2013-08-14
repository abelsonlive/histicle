rm(list=ls())
setwd("~/Dropbox/code/histicle/")

d <- read.csv("data/listicles.csv")

par(family="Helvetica Neue")
png(width=800, height=500, file="imgs/histicle.png")
hist(d$list_length[d$list_length<100], 
    breaks=50,
    col="darkblue",
    border="white",
    main="Distribution of Listicle Lengths",
    xlab="Listicle Length")
dev.off()