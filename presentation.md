# FILM SEASONALITY

## Background

Every industry contains a certain set of unwritten rules or stories that identify standard behaviors and set out what it takes to make money. In the film industry, one of the most common and pervasive of these rules is that the season in which a film is released has an outsized effect on the chances of its success. Studios have created stories (as in mental narratives that state a perspective on how the world works) about consumer behaviors and the relationship between those behaviors and the probability of success for any particular film. 

These stories, however, aren’t necessarily evaluated for their validity; they are the result of decades of releasing movies in this pattern. Further, these stories are reinforced by reality; since a studio will only try to release a film they expect to be a hit during a window in which they think it will become one, hits generally occur (or are perceived to occur) during those windows.

These beliefes are why we see many big budget, super-hero movies released back to back in early summer and none released during the month of September. Recently, there have been some counter-examples to this trend. The most prominent of these counter-examples is likely Deadpool, which was released Feb 12, 2016. Typically, a blockbuster, super-hero, based on a comic book movie would be slated for the summer or the holidays and would avoid releasing on or around something like Valentine’s Day (or in the lead-up to Spring Break). Despite the ‘headwinds’, Deadpool greatly outperformed expectations, bringing in more than $750M in worldwide box office.

For another example, per the movie tracking website The Numbers:
- Since 1990, there have been 77 films released that:
    - Are G-rated
    - Were made in the US
    - Have a budget of at least $1M
- Of these films, over 43% have been released in June and November.
- Zero have been released in the month of September. Why not? Could it be the case that there is a pervasive belief that kids going back to school won't get to go to the movies?

# THIS IS FOR YOU KAYLA
![Pie chart of G-rated releases](https://github.com/sizej/Capstone1/blob/master/images/forkayla.jpeg)

## The Data

This dataset was scraped from IMDB. It contains over 80,000 movies from all over the world going back to 1910. For the purposes of this analysis, the salient features are:
- Financials
    - Budget - how much did the film cost to produce (not including marketing or other overhead costs)
    - Worldwide Gross - how much did the film take in from theaters worldwide
- Release date - when was the film released
- Genre - IMDB classifies a film into one or more of 18 genres. However, each film has no more than 3 genre classifications.

In order to understand the effects of seasonality on film performance, I filtered out the vast majority of films from the dataset. The filters were:
- The film must have a reported budget without which the could be no analysis of profitability/performance.
- The film's budget must be denominated in USD. Foreign-produced films are beyond the scope of this analysis.
- The film must have a reported US Gross revenue. If a film was made here, but never released here, it is also beyond the scope of this analysis.
- The film was released in 1970 or later. This cuts out the oldest 120 movies - from a time when far fewer films came out and there was much less competition.
The resulting dataset is some 7100 films, dating from 1970 to 2019.

## Initial Observations

Total revenue over the course of the year

Total budget over the course of the year

Count of Releases over the course of the year

In some ways, the movie business is resistant to analysis of raw numbers; real success is all about outliers. It only takes one *Titanic* to pay for a lot of *Sharknados*. 

For example, the most profitable week of the year is week 50 (Christmas week). In the dataset, there are 133 films released in week 50, but **about 20% (or roughly $5B) of the total profit** of that week is attributable to two films, *Avatar* and *Star Wars: Episode VII*. Massive hits are by definition outliers (and outliers are hard to predict or analyze). Further, even focusing on 'return' alone can be challenging. For example, *The Blair Witch Project* made ~$250M on its paltry $60k budget (roughly a 416,667% return).

Thus, for the purposes of this analysis, it makes more sense to focus on commercial success - that is, sufficient return on the investment. Using both my own experience and a small survey of people in the industry, I landed on a threshold of three times the budget in order for a film to be considered commercially successful.

**The big question is whether or not seasonality drives film success more than supply, or at least whether they are close to equally important**

## Hypothesis Test #1 - Prime Window

| Status | Successes | Attempts | Success Rate |
| --- | --- | --- | --- |
| Prime | 660 | 2143 | 0.308 |
| Not Prime | 1328  | 4973 | 0.267 |

1. Null hypothesis is that prime window success rate is equal to not prime window success rate. Alternative hypothesis is that the prime window success rate is greater than not prime.

2. One tailed z-test, alpha = 0.05

3. z-score = 3.53, test_statistic = 0.0004

4. Reject the null - prime window does outperfom not prime window

## Hypothesis Test #2 - Competitive Effect

To examine the role of supply (or competition) in film success, I used the count of films released the week before, the week of, and the week after a film's release, so for every film in the dataset, we know how many 'competitors' it has. I chose this window because the lion's share of a film's theatrical revenue comes in the first two weekends. I chose to break the dataset into three parts - low competition (~27%), high competition (~25%), and middle competition (~48%). 

![Histogram of competitors](images/competitor_hist.jpeg)

| Competition | Successes | Attempts | Success Rate |
| --- | --- | --- | --- |
| Low | 362 | 943 | 0.384 |
| Middle | 916 | 3287 | 0.279 |
| High | 710 | 2886 | 0.246 |


I then performed two hypothesis tests - low vs. middle and high vs. middle. Since I am doing two comparisons, I used an alpha of 0.025 (Bonferroni correction for an alpha of 0.05).

#### Hypothesis Test #2A - Low v. Middle

1. Null Hypothesis: Success rate for low competition films is equal to success rate for middle competition films. Alternate hypothesis is that low competition films outperform middle competition films.

2. One tailed z-test, alpha = 0.025

3. z-score = 6.229, test_statistic = 2.344e-10

4. Reject the null - low competition films outperform middle competition films.

#### Hypothesis Test #2B - High v. Middle

1. Null Hypothesis: Success rate for high competition films is equal to success rate for middle competition films. Alternate hypothesis is that high competition films underperform middle competition films.

2. One tailed z-test, alpha = 0.025

3. z-score = -2.908, test_statistic = 0.002

4. Reject the null - high competition films underperform middle competition films.

That seasonality and competitive set are significant is (potentially) unsurprising. The surprising thing was how significant the results were, which led me to consider why this might the case. The first thing that came to mind was time. Older films have much higher success rates:

![Success Rate over time](images/years.jpeg)

Indeed, the mean year for the low competititon films is 1986; for the high competition films, the mean year is 2008.

#### Hypthesis Test #3 - Competitive Effect - Films since 2000

I filtered down the dataset to just films released this century. 
