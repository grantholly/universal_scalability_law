## Simple Universal Scalability Law Example
###################

library(dplyr)
library(reshape2)
library(ggplot2)

# read in the dataset
data <- read.csv('output/factors.csv')

# IF NECESSARY, convert from 'duration' to 'throughput'
workload <- 500
data <- summarize(group_by(data, cores), throughput = workload / mean(duration))

# compute data to be modeled
data$capacity <- data$throughput / data$throughput[1]
data$invEff <- data$cores / data$capacity
data$additionalCores <- data$cores - 1
data$additionalInvEff <- data$invEff - 1

# visualize data to be modeled
plot(data$additionalCores, data$additionalInvEff)

# fit a quadratic model to the data
fit <- lm(additionalInvEff ~ poly(additionalCores, 2, raw = TRUE), data = data)
summary(fit)

# compute the USL coefficients and define the function
alpha <- as.numeric(fit$coefficients[2] - fit$coefficients[3])
beta <- as.numeric(fit$coefficients[3])
usl <- function(x) { x / (1 + alpha * (x - 1) + beta * x * (x - 1)) }

# use USL to compute predicted capacity/throughput
data$predictedCapacity <- usl(data$cores)
data$predictedThroughput <- data$predictedCapacity * data$throughput[1]

# compute the value at which capacity/throughput is optimized
nOpt <- sqrt((1 - alpha) / beta)

# plot predicted v. observed
plotData <- melt(data[, c(1, 2, 8)], id.vars = 1, variable.name = "label", value.name = "throughput")
g <- ggplot(plotData, aes(x = cores, y = throughput, color = label)) + geom_point()
g <- g + ggtitle(paste("Modeled throughput: NMax = ", round(nOpt)))
g
