import collections
import numpy as np
import pandas as pd
import re
from patsy import dmatrices


def movies(filepath):
    '''
    Converts raw data in movies.dat download file (of form 
    "<MovieID><Title><MoviePopularity>", as noted in Tag Genome README)
    to pandas DataFrame. 
    
    Separates movie title and release year into two separate columns for 
    easier manipulation down the line.
    
    Substitutes `0` for missing years. 
    
    Parameters
    ----------
    filepath : .dat file 
        MovieID, Title (and year), MoviePopularity (i.e., number of 
        ratings on MovieLens) for movies in MovieLens Tag Genome. 

    Returns
    -------
    movies_df : DataFrame
        MovieID, NumRatings, and ReleaseYear for movies in 
        MovieLens Tag Genome. Titles are indices.
    '''
    movies_df = pd.read_csv(filepath, sep='\t', header=None, 
                            names=['MovieID', 'Title', 'NumRatings'])

    release_year = movies_df['Title']
    release_year = [year[year.find('(')+1:year.find(')')] 
                   for year in release_year]
    release_year = [re.sub('[^0-9]','', year) for year in release_year]
    release_year = [int(year) for year in release_year if year != '']
    release_year = pd.Series(release_year)
    
    movies_df['ReleaseYear'] = release_year
    movies_df['ReleaseYear'] = movies_df['ReleaseYear'].fillna(0)
    movies_df['ReleaseYear'] = movies_df['ReleaseYear'].astype(int)
    movies_df['Title'] = movies_df['Title'].str[:-6] 
    titles = movies_df.pop('Title')
    movies_df.index = titles

    return movies_df

def tags(filepath):
    '''
    Converts raw data in tags.dat download file (of form 
    "<TagID><Tag><TagPopularity>", as noted in Tag Genome README)
    to pandas DataFrame. 
    
    Separates movie title and release year into two separate columns for 
    easier manipulation down the line.
    
    Parameters
    ----------
    filepath : .dat file 
        TagID, Tag name, and TagPopularity (i.e., number of taggings on
        MovieLens) for tags in MovieLens Tag Genome. 

    Returns
    -------
    tags_df : DataFrame
        TagID, NumTaggings for tags in MovieLens Tag Genome. 
        Tags are indices.
    '''
    
    tags_df = pd.read_csv(filepath, sep='\t', header=None, 
                        names=['TagID', 'Tag', 'NumTaggings'])
    tag_names = tags_df.pop('Tag')
    tags_df.index = tag_names
    return tags_df

def tag_relevance(filepath):
    '''
    Converts raw data in tag-relevance.dat download file (of form 
    "<MovieID><TagID><Relevance>", as noted in Tag Genome README)
    to pandas DataFrame. 
    
    Separates movie title and release year into two separate columns for 
    easier manipulation down the line.
    
    Parameters
    ----------
    filepath : .dat file 
        MovieID, TagID, and Relevance (0-1 relevance score for tags)
        for movies and tags in MovieLens Tag Genome. 

    Returns
    -------
    tag_relevance_df : DataFrame
        MovieID, TagID, TagRelevance for movies and tags in MovieLens 
        Tag Genome. 
    '''
    
    tag_relevance_df = pd.read_csv(filepath, sep='\t', header=None, 
                        names=['MovieID', 'TagID', 'TagRelevance'])
    return tag_relevance_df

def popularity(tags_or_movies_df, top_percent):
    '''Sorts tags or movies in a dataframe according to the number of 
    times each has been tagged or rated. Returns top percent of tags 
    or movies.
    
    Parameters
    ----------
    tags_or_movies_df : DataFrame
        Either the DataFrame of tags or that of movies.
    top_percent : float
        Decimal percentage of movies or tags to return, 
        based on popularity.

    Returns
    -------
    by_pop : DataFrame
        TagID or MovieID;  ReleaseYear; and NumTaggings or NumRatings
        for Tags or Titles.
    '''   
    headers = tags_or_movies_df.columns.tolist()
    
    try:
        if len(headers) == 2:
            by_pop = tags_or_movies_df.sort_values(
                'NumTaggings', ascending=False)
            print 'Computing top ' + str(cutoff) + ' tags.'
        if len(headers) == 3:
            by_pop = tags_or_movies_df.sort_values(
                'NumRatings', ascending=False)
            print 'Computing top ' + str(cutoff) + ' titles.'
        
        cutoff = int(float(len(by_pop)) * top_percent)
        by_pop = by_pop[:cutoff]
        return by_pop
        
    except Exception:    
        print 'Input either `movies` or `tags` DataFrame.' 