Sam Panzer (panzers) and Cory Rivera (rcor)

We set the learning rate to 0.01 / (# features), because we wanted a small alpha that was inversely proportional to the number of features, as suggested in the homework.

The discount was set to 1, since we wanted a fairly neutral value.

Rewards were as follows:
  - food_reward = 2.0, to emphasize searching for food.
  - killer_reward = 0.3, because killing another ant can be worth it occasionally.
  - death_reward = -0.8, because we want to avoid death, but it isn't the worst possible thing.

Our exploration-exploitation strategy was a linearization of the suggested strategy. We explored for 15 games, decreased the exploration probability linearly until it hit zero at 30 games, then exploited for the last few games. We wanted to follow the suggestion, but wanted it to be a little more controlled.

The most negative features were (in order of decreasing magnitude):
  [number of nearby friendly ants (our new feature!), Closest enemy far (>4) away, closest food far (>4) away].
The most positive weights were (in decreasing order):
  [Friendly adjacent + closest food far away, moving towards closest food + closest enemy far away,  closest food 1 away]

Our new feature was a very easy one to implement: the number of friendly ants within a 4-cell radius. The theory was that we don't want our ants to cluster too much, so if this value was high, it should encourage exploration, but it shouldn't have too much of an effect if the "friendly neighbors" value was low. We expected the weight to be negative - but not the *most* negative.
