## 1. Research Questions From Videos

**Question 1: How much does a fielder's momentum affect throw velocity?**

Turang throws the ball much harder than Altuve in these two clips. While Turang has more arm strength, I also noticed his momentum is moving much closer to first base than Altuve's. By getting around the ball better, Turang was able to redirect his momentum closer to the bag and potentially get more velocity on the throw.

Isolating momentum's effect on velocity would be a good way to give credit to fielders who have better footwork or move faster. I would pull player tracking data from Hawkeye in addition to throw velocity, exchange time, and runner speed. By tracking runner speed as the runner closes in on the bag, I could filter for close plays.

The result would be a metric similar to Statcast's outfield jump. I would measure the fielder's speed, acceleration, and direction (relative to 1b) as they move through the ball and into the throw. The throw would be measured relative to the fielder's max velocity to see how much his movement influenced it.

**Question 2: How much throw velocity does a fast exchange cost?**

Altuve has a quick exchange in his clip, but the throw is quite soft. Quicker exchanges normally result in less velocity so that makes sense. Measuring the relationship between exchange time and velocity could provide meaningful insight.

To measure it, I would gather the exchange time, velocity, and runner speed. Runner speed would be used similarly to the previous question as a means of filtering for competitive plays.

By measuring this relationship, front offices could identify outlier results where players are able to minimize the loss of velocity from faster exchanges. This could be used to identify players that may have higher outs above average.

## 2. Swing Decision Metric

Good swing decisions are not universal. Hitters have different strengths and weaknesses, and their swing decisions need to be viewed from that context. The model would calculate expected run values based off hitter swing decisions.

The features would be the following:

- Pitch location relative to the hitter's zone
- Pitch type
- Velocity
- Pitch shape (IVB, HB)
- Count
- Pitcher handedness
- Batter handedness
- Batter identity

This feature set would give the model sufficient context to determine how likely the hitter is to have a positive result if he chooses to swing. The model would use this context to calculate expected run values for a swing and a take respectively. I would then use the following formula to create a swing advantage metric:

`swing advantage = swing xRV - take xRV`

If the hitter swings, he gets the swing advantage. If he takes, he gets the swing advantage negated. This metric would determine if swinging or taking is the right decision. Averaging over all the hitter's pitches would give a score, and the metric could be scaled where 100 is average and +/- 10 is 1 standard deviation. The stat could also measure how good a hitter's decisions were for a single game.

To validate the model, I would test the predictive value of the metric compared to more traditional swing decision metrics like chase rate or zone-swing rate. If my metric is more predictive of something like next season's wOBA than those traditional metrics, it could be inferred that the metric is capturing meaningful information.

## 3. Lower Mound

Lowering the mound would primarily influence the verticality of pitches coming in. As such, it would affect pitchers relying on that more than those that rely on horizontal break. For pitchers that try to pitch above the barrel with four seams, I would expect that they would probably be a little better as the VAA of their pitches would likely flatten out slightly.

Conversely, the same thing helping those pitchers would hurt sinker ballers. Because of the flatter angle, it is likely that sinker ballers would generate fewer ground balls and get hit a little harder.

It is worth noting that some pitchers are able to pitch over the barrel because of exceptional velocity rather than a flat VAA. Those pitchers might fare a little worse since most pitchers would probably lose a small amount of velocity.

The change in VAA could be calculated mathematically by lowering the release point by two inches which would be useful when projecting the effect. That being said, it would not capture any potential movement differences that might arise from the lower mound. As such, the best way to measure differences would be to gather pitch data from guys throwing on the lower mound in the offseason.

If I were able to get data from that, I would see what else changed like stride length, extension, arm slot, etc. After that, I could take the pitcher's arsenal data from the previous year and calculate the projected changes. Those projected changes would then be scored using run value (stuff+) to determine if the pitcher's arsenal got better or worse.

I would also compare the pitcher's projected changes with league-wide projected changes. If a pitcher is projected to get 1 percent worse, but the league is projected to get 3 percent worse, that pitcher effectively got better.

To validate the projections, I would compare them to actual 2027 pitch data as it starts coming in. Since pitch characteristics are very stable, the model could be refined very early in the season.

## 4. Swing-and-Miss Model

I'd use a gradient boosted model (XGBoost or LightGBM) to measure the relationships between pitch characteristics and generate an expected whiff percentage for the pitch.

For training, 1 would represent a whiff and 0 would represent everything else. The easiest way to test the model is to have it predict whiffs on a season it didn't see in training. So the model would be trained on multiple previous seasons and tested on the last full season.

Validating the model would be done by comparing the predicted values to the actual values on the test season. This can be done using metrics like log loss and root mean squared error (RMSE).

The feature set provided should produce respectable results, but I do think there are some meaningful ones to be added. Those are listed here:

- Count
- VAA
- HAA
- Release point
- Batter handedness
- Pitcher handedness
- Differential variables

The differential variables would measure the difference in pitch characteristics like velocity or break compared to the pitcher's average fastball. These features could be added individually and measured against the base model to see if they made it better or worse.

Changing the model to run value could give more credit to contact pitchers. The model could be constructed pretty much identically to the previous model. The only change would be the target variable. Rather than targeting whiffs, the model would target the change in run value from pitch to pitch.

I wrote an article about models I built similar to these and linked it below. The biggest difference is that the models I wrote about purposely excluded pitch location in order to measure pitch characteristics alone.

Link: https://medium.com/@connerhammonds/pitch-grading-providing-quantitative-metrics-to-guide-players-34cbd48f3b3f

## 5. Wild Card Probabilities

**Output:**

| Order (1st to 4th) | Probability |
|--------------------|-------------|
| CHC, PHI, SD, ARI  | 31.93%      |
| PHI, CHC, SD, ARI  | 21.29%      |
| CHC, PHI, ARI, SD  | 8.90%       |

Code: `wild_card_orders.py`

To start, I needed to calculate the number of remaining games for each team. This was done by taking 162 and subtracting the sum of the team's wins and losses.

After that, I used the win probabilities from the prompt to calculate the probability of every possible combination among the four teams. This was done by multiplying the probability that each team reaches its win total together. There were 74,360 different combinations in total.

To calculate the probability of a certain order occurring, I found every combination that resulted in the same final order and added their probabilities together. Tiebreakers were decided by standings order (as directed). I added those order probabilities to a table and sorted them in descending order. Lastly, the script displays the top three probabilities.

The only assumption that was made is that all 162 games would be played.

## 6. Expected Runs Per Game

Code: `expected_runs.py`

Answer: 2.34 runs per game or 0.26 runs per inning.

Each inning was split into 24 different possible combinations representing base-out states. I made a run expectancy table to calculate the expected number of runs for each of the 24 different combinations using the probabilities in the prompt.

To calculate the run expectancy, I used the following formula:

`Run expectancy (current situation) = Σ (probability of outcome) x (runs scored on the play + run expectancy (next situation))`

In this case, the summation means that I added those expected run values for each outcome (walk, HR, fly out, strikeout) together to get the total run expectancy for the situation.

Because some outcomes (walks and homers) don't add an out, some of the situations depend on other situations. To determine what the right values are, I started every run expectancy at 0 and calculated new run expectancies. Each time I calculated a new run expectancy, I replaced the old one. I looped that until the values stabilized which happened after about 20 loops.

Games are 9 innings long and every inning starts with the same base-out state. To calculate the answer, I just took the run expectancy for 0 outs with bases empty which was 0.26 and multiplied it by 9.

As far as assumptions go, I assumed that fly outs didn't result in runs when there were 2 outs. I also assumed the team bats in all 9 innings.



