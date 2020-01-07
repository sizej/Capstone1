# FILM SEASONALITY

## Background


Per the movie tracking website The Numbers:
- Since 1990, there have been 77 films released that:
    - Are G-rated
    - Made in the US
    - Have a budget of at least $1M
- Of these films, over 43% have been released in either November or June.
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
The resulting dataset is some 7200 films, dating from 1920 to 2019.

## Initial Observations

Total revenue over the course of the year

Total budget over the course of the year

In some ways, the movie business is resistant to analysis of raw numbers; real success is all about outliers. It only takes one *Titanic* to pay for a lot of *Sharknados*. 

For example, the most profitable week of the year is week 50 (Christmas week). In the dataset, there are 133 films released in week 50, but **about 20% (or roughly $5B) of the total profit** of that week is attributable to two films, *Avatar* and *Star Wars: Episode VII*. Massive hits are by definition outliers (and outliers are hard to predict or analyze).

For the purposes of this analysis, it makes more sense to focus on commercial success - that is, a good return on the investment. Using both my own experience and a small survey of people in the industry, I landed on a threshold of three times the budget in order for a film to be considered commercially successful.


**The big question is whether or not seasonality drives film success more than supply, or at least whether they are close to equally important**