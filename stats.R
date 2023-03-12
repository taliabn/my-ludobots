med.0 <- as.matrix(read.csv("NH-stats-0-medians.csv", col.names=c("0"))*-1)
best0.1 <- as.matrix(read.csv("NH-stats-0-best1.csv", col.names=c("0"))*-1)
best0.5 <- as.matrix(read.csv("NH-stats-0-best5.csv", col.names=c("0"))*-1)

med.1 <- as.matrix(read.csv("NH-stats-1-medians.csv", col.names=c("1"))*-1)
best1.1 <- as.matrix(read.csv("NH-stats-1-best1.csv", col.names=c("1"))*-1)
best1.5 <- as.matrix(read.csv("NH-stats-1-best5.csv", col.names=c("1"))*-1)

med.2 <- as.matrix(read.csv("NH-stats-2-medians.csv", col.names=c("2"))*-1)
best2.1 <- as.matrix(read.csv("NH-stats-2-best1.csv", col.names=c("2"))*-1)
best2.5 <- as.matrix(read.csv("NH-stats-2-best5.csv", col.names=c("2"))*-1)


# t tests
t.test(med.0, med.2, alternative="two.sided", paired=FALSE)
t.test(med.0, med.1, alternative="two.sided", paired=FALSE)
t.test(med.1, med.2, alternative="two.sided", paired=FALSE)

t.test(med.0, med.2, alternative="less", paired=FALSE)
t.test(med.0, med.1, alternative="less", paired=FALSE)
t.test(med.1, med.2, alternative="less", paired=FALSE)

t.test(best0.1, best1.1, alternative="two.sided", paired=FALSE)
t.test(best0.1, best2.1, alternative="two.sided", paired=FALSE)
t.test(best1.1, best2.1, alternative="two.sided", paired=FALSE)

t.test(best0.1, best1.1, alternative="less", paired=FALSE) # diff
t.test(best0.1, best2.1, alternative="less", paired=FALSE)
t.test(best1.1, best2.1, alternative="less", paired=FALSE)


t.test(best0.5, best1.5, alternative="two.sided", paired=FALSE)
t.test(best0.5, best2.5, alternative="two.sided", paired=FALSE)
t.test(best1.5, best2.5, alternative="two.sided", paired=FALSE)

t.test(best0.5, best1.5, alternative="less", paired=FALSE)
t.test(best0.5, best2.5, alternative="less", paired=FALSE) # 0.076
t.test(best1.5, best2.5, alternative="less", paired=FALSE)

# wilcox tests
wilcox.test(med.0, med.2, alternative="two.sided", paired=FALSE)
wilcox.test(med.0, med.1, alternative="two.sided", paired=FALSE)
wilcox.test(med.1, med.2, alternative="two.sided", paired=FALSE)

wilcox.test(med.0, med.2, alternative="less", paired=FALSE)
wilcox.test(med.0, med.1, alternative="less", paired=FALSE)
wilcox.test(med.1, med.2, alternative="less", paired=FALSE)


wilcox.test(best0.1, best1.1, alternative="two.sided", paired=FALSE)
wilcox.test(best0.1, best2.1, alternative="two.sided", paired=FALSE)
wilcox.test(best1.1, best2.1, alternative="two.sided", paired=FALSE)

wilcox.test(best0.5, best1.5, alternative="less", paired=FALSE)
wilcox.test(best0.5, best2.5, alternative="less", paired=FALSE) # 0.90
wilcox.test(best1.5, best2.5, alternative="less", paired=FALSE)


boxplot(c(best0.5), c(best1.5), c(best2.5), names=c("0", "1", "2"), 
        main="Best 5 final fitnesses for each seed", 
        xlab="Number of hidden layers", ylab ="Best ending fitness")
