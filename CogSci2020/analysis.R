"""
Crowdsourcing to analyze belief systems underlying social issues
J. Hunter Priniski and Keith Holyoak

Description:
Analysis script
"""

require(tidyverse)
require(SnowballC)
library(readr)
require(brms)
require(rstan)
require(Rcpp)
require(scales)
require(gridExtra)
require(loo)
require(tidyverse)
require(readxl)
rstan_options(auto_write = TRUE)
options(mc.cores = parallel::detectCores())

data_coded <- read_csv("data_coded.csv")

data_coded2 <- data_coded%>%
  filter(Position != 0)%>%
  mutate(Position = factor(Position))%>%
  mutate(Position = ifelse(Position == 1, 'For', 'Against'))%>%
  mutate(category = ifelse(category == 'MORAL','Moral',ifelse(category == '_STOPWORD', '_StopWord', 'Statistical')))%>%
  filter(category != '_StopWord')


model1 <- brm(category ~  Position + (1 | postid),
              data=data_coded2,
              family="categorical", 
              file = 'model1',
              chains=4, 
              iter=3000, 
              warmup=1500,
              control = list(adapt_delta = .90),
              prior = c(set_prior("normal(0, 1)", class = "b", coef = "PositionFor", dpar = 'muStatistical'),
                        set_prior("normal(1,2)", class= "sd", dpar = 'muStatistical')))

ce <- conditional_effects(model1, effects = 'Position', categorical = T)

plot(ce, theme=theme_bw(10))

#look at moral word types
data_coded3$instance <- as.integer(instance)
vals <- data_coded3$instance %% 2 == 0
data_coded3 <- data_coded2%>%
  filter(category == 'Moral')%>%
  mutate(`Moral Construct`=recode(instance,
                                  `1` = 'Care',
                                  `2` = 'Care',
                                  `3` = 'Fairness',
                                  `4` = 'Fairness',
                                  `5` = 'Loyalty',
                                  `6` = 'Loyalty',
                                  `7` = 'Authority',
                                  `8` = 'Authority',
                                  `9` = 'Sanctity',
                                  `10` = 'Sanctity'))%>%
  mutate(`Type` = ifelse(vals, 'Vice', 'Virtue'))

ggplot(data_coded3, aes(`Moral Construct`))+
  geom_bar()+
  facet_wrap(~`Type`)+
  labs(y ="Number of Uses in Corpus")+
  theme_bw(12)








  