#!/usr/bin/env python3
# coding: utf-8
import yaml
import os
import datetime
import scholarly


def load_yaml_file(fname):

    if hasattr(yaml, "FullLoader"):
        kwargs = dict(Loader=yaml.FullLoader)
    else:
        kwargs = {}

    if os.path.isfile(fname):
        with open(fname, "r") as f:
            d = yaml.load(f, **kwargs)
    else:
        d = {}
    return d


def dump_yaml(data, fname):
    with open(fname, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


def compute_todays_impact(history_file, people_file):

    # Import input data
    people = load_yaml_file(people_file)

    # Load database
    history = load_yaml_file(history_file)

    publications = extract_scholar_publications(people)

    # Compute impact and h-index
    num_cites = impact(publications)
    h = h_index(publications)

    # Find shooting star papers
    max_years = 5
    N_all_stars = 5
    N_rising_stars = 3
    all_stars_ = all_stars(publications, N=N_all_stars)
    rising_stars_ = rising_stars(publications, N=N_rising_stars, max_years=max_years)

    # Add new input to history and dump to database
    today = datetime.datetime.now().date().isoformat()
    history[today] = dict(
        num_cites=num_cites, h_index=h, all_stars=all_stars_, rising_stars=rising_stars_
    )

    dump_yaml(history, history_file)

    # Create output mesage
    message = []
    message += [f"Your impact today is {num_cites}. Well done!"]
    message += [f"Your h-index today is {h}. Awesome!"]
    message += [f"*The all stars (most cited-per-year papers (all time)) are*:"]
    for (title, cites) in all_stars_:
        message += [f"{N_all_stars}: {title} ({cites:2.1f})"]
        N_all_stars = N_all_stars - 1
    message += [
        f"\n*The rising stars (most cited-per-year papers not older than {max_years} years) are*:"
    ]
    for (title, cites) in rising_stars_:
        message += [f"{N_rising_stars}: {title} ({cites:2.1f})"]
        N_rising_stars = N_rising_stars - 1
    return "\n".join(message)


def extract_scholar_publications(people):
    publications = {}
    for person, id_ in people.items():

        if id_ == "":
            continue
        print(person, id_)
        query = scholarly.search_author(person)
        for q in query:
            if q.id == id_:
                info = q.fill()
                # print([p.bib['title'] for p in info.publications])
                # print('\n\n')
                publications[id_] = info.publications
                break
    return publications


def unique_titles_vs_citations(publications):
    "Extract unique titles and corresponding number of citations."
    titles = {}
    for (id_, pubs) in publications.items():
        for p in pubs:
            try:
                titles[p.bib["title"]] = p.citedby
            except AttributeError:
                titles[p.bib["title"]] = 0

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
        if (i + 1) > num_cites:
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
            if not "year" in p.bib:
                continue
            years = (year - p.bib["year"]) + 1
            if hasattr(p, "citedby"):
                try:
                    titles[p.bib["title"]] = p.citedby / years
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
            if not "year" in p.bib:
                continue
            years = (year - p.bib["year"]) + 1
            if years > max_years:
                continue
            if hasattr(p, "citedby"):
                try:
                    titles[p.bib["title"]] = p.citedby / years
                except:
                    continue

    # Print top N paper (cited most per year):
    stars = sorted(titles.items(), key=lambda x: (x[1], x[0]))[-N:]
    return list(stars)

