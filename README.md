Functions for dealing with data from the MovieLens Tag Genome Dataset (http://grouplens.org/datasets/movielens/tag-genome/). 

So far: functions to read in the three files that make up the Dataset into pandas DataFrames, as well as a function to sort and filter movies and tags by popularity. 

To come: functions for modeling a given tag's correlations with other tags, and a given movie's correlations with other movies.


To run: 

- Download the MovieLens Tag Genome Dataset from http://grouplens.org/datasets/movielens/tag-genome/. The Dataset comes downloaded as a zip of three files: movies.dat, tags.dat, and tag-relevance.dat.

- Run the movies, tags, and tag_relevance functions, which take in the downloaded files and return pandas DataFrames.
```
import mltg
mltg.movies([path_to_movies.dat]) 
mltg.tags([path_to_tags.dat])
mltg.tag_relevance([path_to_tag_relevance.dat])
```
- (Optional:) sort movies and/or tags by popularity. Returns a DataFrame containing the top_percent of tags or movies.
```
mltg.popularity(tags_or_movies_df, top_percent)
```
