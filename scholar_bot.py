#!/usr/bin/env python3
# coding: utf-8
import yaml
import datetime
import scholarly


def extract_scholar_publications(people):
    publications = {}
    for person, id_ in people.items():

        if id_ == '':
            continue
        try:
            info = next(scholarly.search_author(person)).fill()
        except StopIteration:
            print(f'Publications not found for {person}')
        publications[id_] = info.publications
    return publications


def unique_titles_vs_citations(publications):
    "Extract unique titles and corresponding number of citations."
    titles = {}
    for (id_, pubs) in publications.items():
        for p in pubs:
            try:
                titles[p.bib['title']] = p.citedby
            except AttributeError:
                titles[p.bib['title']] = 0
            
    return titles

def impact(publications):
    """Compute the impact (total number of unique citations) from
    publications."""
    
    # Extract unique titles with corresponding number of citations
    titles = unique_titles_vs_citations(publications)

    # Compute total number of citations
    num_cites = sum(titles.values())
    return num_cites

def h_index(publications):
    "Compute the h_index of the combined lists of publications."

    # Extract unique titles with corresponding number of citations
    titles = unique_titles_vs_citations(publications)

    # Sort list of num of citations in descending order
    cites = reversed(sorted(titles.values()))

    # Compute the h-index
    for (i, num_cites) in enumerate(cites):
        if (i+1) > num_cites:
            break
    h_index = i

    return h_index

def all_stars(publications, N=5):
    "Compute the N papers with most citations per year."

    # Find the current year
    year = datetime.date.today().year

    # Iterate through all papers and compute number of citations per year
    titles = {}
    for (id, pubs) in publications.items():
        for p in pubs:
            if not 'year' in p.bib:
                continue
            years = (year - p.bib['year']) + 1
            if hasattr(p, 'citedby'):
                try:
                    titles[p.bib['title']] = p.citedby/years
                except:
                    continue

    # Print top N paper (cited most per year):
    stars = sorted(titles.items(), key=lambda x: (x[1], x[0]))[-N:]
    return list(stars)

def rising_stars(publications, max_years=5, N=3):
    "Compute the N papers with most citations per year not older than max_years."

    # Find the current year
    year = datetime.date.today().year

    # Iterate through all papers and compute number of citations per year
    titles = {}
    for (id, pubs) in publications.items():
        for p in pubs:
            if not 'year' in p.bib:
                continue
            years = (year - p.bib['year']) + 1
            if years > max_years:
                continue
            if hasattr(p, 'citedby'):
                try:
                    titles[p.bib['title']] = p.citedby/years
                except:
                    continue

    # Print top N paper (cited most per year):
    stars = sorted(titles.items(), key=lambda x: (x[1], x[0]))[-N:]
    return list(stars)

