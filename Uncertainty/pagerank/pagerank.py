# import os
# import random
# import re
# import sys
#
# DAMPING = 0.85
# SAMPLES = 10000
#
#
# def main():
#     if len(sys.argv) != 2:
#         sys.exit("Usage: python pagerank.py corpus")
#     corpus = crawl(sys.argv[1])
#     ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
#     print(f"PageRank Results from Sampling (n = {SAMPLES})")
#     for page in sorted(ranks):
#         print(f"  {page}: {ranks[page]:.4f}")
#     ranks = iterate_pagerank(corpus, DAMPING)
#     print(f"PageRank Results from Iteration")
#     for page in sorted(ranks):
#         print(f"  {page}: {ranks[page]:.4f}")
#
#
# def crawl(directory):
#     """
#     Parse a directory of HTML pages and check for links to other pages.
#     Return a dictionary where each key is a page, and values are
#     a list of all other pages in the corpus that are linked to by the page.
#     """
#     pages = dict()
#
#     # Extract all links from HTML files
#     for filename in os.listdir(directory):
#         if not filename.endswith(".html"):
#             continue
#         with open(os.path.join(directory, filename)) as f:
#             contents = f.read()
#             links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
#             pages[filename] = set(links) - {filename}
#
#     # Only include links to other pages in the corpus
#     for filename in pages:
#         pages[filename] = set(
#             link for link in pages[filename]
#             if link in pages
#         )
#     return pages
#
#
# def transition_model(corpus, page, damping_factor):
#     """
#     Return a probability distribution over which page to visit next,
#     given a current page.
#
#     With probability `damping_factor`, choose a link at random
#     linked to by `page`. With probability `1 - damping_factor`, choose
#     a link at random chosen from all pages in the corpus.
#     """
#
#     """
#     This function gives a page, asking the distribution over that page chosen for next page.
#     Only one page is analyzed
#     """
#     page_dist = {}
#     # For page that has no link: (evenly choose next from all)
#     if len(corpus[page]) == 0:
#         even_dist = 1 / (len(corpus))
#         for x in corpus:
#             page_dist[x] = even_dist
#
#     # probability of choosing in random (d)
#     random_prob = (1 - damping_factor) / (len(corpus))
#
#     # probability of choosing from links
#     links_prob = damping_factor / (len(corpus[page]))
#
#     for x in corpus:
#         if x in corpus[page]:
#             page_dist[x] = random_prob + links_prob
#         else:
#             page_dist[x] = random_prob
#     return page_dist
#
#
# def sample_pagerank(corpus, damping_factor, n):
#     """
#     Return PageRank values for each page by sampling `n` pages
#     according to transition model, starting with a page at random.
#
#     Return a dictionary where keys are page names, and values are
#     their estimated PageRank value (a value between 0 and 1). All
#     PageRank values should sum to 1.
#     """
#     pageRank = dict()
#     hit_num = {x: 0 for x in corpus}
#     current_page = random.choice(corpus)
#     hit_num[current_page] = 1
#     for i in range(1, n):
#         dist_page = transition_model(corpus, current_page, damping_factor)
#         page_list = []
#         prob_list = []
#         for keys, values in dist_page.items():
#             page_list.append(keys)
#             prob_list.append(values)
#         current_page = random.choices(page_list, weights=prob_list)
#         hit_num[current_page] += 1
#     for i in hit_num:
#         pageRank[i] = hit_num[i] / n
#     return pageRank
#
#
# def iterate_pagerank(corpus, damping_factor):
#     """
#     Return PageRank values for each page by iteratively updating
#     PageRank values until convergence.
#
#     Return a dictionary where keys are page names, and values are
#     their estimated PageRank value (a value between 0 and 1). All
#     PageRank values should sum to 1.
#     """
#     """
#     # the common component of (1-d)/N
#     random_comp = (1 - damping_factor) / len(corpus.keys())
#
#     pagerank_new = {x: random_comp for x in corpus}
#
#     pagerank_old = {x: random_comp for x in corpus}
#
#     curr_page = random.choice(corpus.key())
#
#     # to determine the convergence
#     diff = 1
#     # iteration number is used for debugging purpose only
#     iteration = 0
#
#     while diff > 0.001:
#         iteration += 1
#         for pages, linked_pages in corpus.items():
#             single_dist = transition_model(corpus, pages, damping_factor)
#             for linked in linked_pages:   # all linked pages for that page
#                 pagerank_new += ((pagerank_new[pages] / len(linked_pages)) * damping_factor)
#         # normalize the rank
#         norm_factor = sum(pagerank_new.values())
#         pagerank_new = {page: (rank / norm_factor) for page, rank in pagerank_new.items()}
#
#         # calculate the new difference
#         diff_new = 0
#         for i in corpus:
#             diff_new += abs(pagerank_new[i] - pagerank_old[i])
#         diff = diff_new
#         # copy new ranks over to old
#         pagerank_old = pagerank_new.copy()
#
#         print("On Iteration ", iteration, " We have diff as ", diff)
#
#     return pagerank_new
#
# """
#     raise NotImplementedError
#
#
# if __name__ == "__main__":
#     main()

import os
import random
import re
import sys

# Damping Factor - probablity that a link is selected from the current page. Otherwise a page from the corpus is switched to at random.
DAMPING = 0.85
SAMPLES = 10000


def main():
    """ Main function to run pagerank algorithm """
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    If a page has no outgoing links, returns an equal probability for all pages in the corpus
    """
    page_dist = {}
    # For page that has no link: (evenly choose next from all)
    if len(corpus[page]) == 0:
        even_dist = 1 / (len(corpus))
        for x in corpus:
            page_dist[x] = even_dist
        return page_dist

    # probability of choosing in random (d)
    random_prob = (1 - damping_factor) / (len(corpus))

    # probability of choosing from links
    links_prob = damping_factor / (len(corpus[page]))

    for x in corpus:
        if x in corpus[page]:
            page_dist[x] = random_prob + links_prob
        else:
            page_dist[x] = random_prob
    return page_dist

    # Initialise probability distribution dictionary:
    """
    prob_dist = {page_name : 0 for page_name in corpus}

    # If page has no links, return equal probability for the corpus:
    if len(corpus[page]) == 0:
        for page_name in prob_dist:
            prob_dist[page_name] = 1 / len(corpus)
        return prob_dist

    # Probability of picking any page at random:
    random_prob = (1 - damping_factor) / len(corpus)

    # Probability of picking a link from the page:
    link_prob = damping_factor / len(corpus[page])

    # Add probabilities to the distribution:
    for page_name in prob_dist:
        prob_dist[page_name] += random_prob

        if page_name in corpus[page]:
            prob_dist[page_name] += link_prob

    return prob_dist
    """


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    """
    visits = {page_name: 0 for page_name in corpus}

    # First page choice is picked at random:
    curr_page = random.choice(list(visits))
    visits[curr_page] += 1

    # For remaining n-1 samples, pick the page based on the transistion model:
    for i in range(0, n-1):

        trans_model = transition_model(corpus, curr_page, damping_factor)

        # Pick next page based on the transition model probabilities:
        rand_val = random.random()
        total_prob = 0

        for page_name, probability in trans_model.items():
            total_prob += probability
            if rand_val <= total_prob:
                curr_page = page_name
                break

        visits[curr_page] += 1

    # Normalise visits using sample number:
    page_ranks = {page_name: (visit_num/n) for page_name, visit_num in visits.items()}

    print('Sum of sample page ranks: ', round(sum(page_ranks.values()), 4))

    return page_ranks
    """
    pageRank = dict()
    hit_num = {x: 0 for x in corpus}
    current_page = random.choice(list(corpus.keys()))
    hit_num[current_page] = 1
    for i in range(1, n):
        dist_page = transition_model(corpus, current_page, damping_factor)
        page_list = []
        prob_list = []
        for keys, values in dist_page.items():
            page_list.append(keys)
            prob_list.append(values)
        current_page = random.choices(page_list, weights=prob_list, k=1)[0]
        hit_num[current_page] = hit_num[current_page] + 1
    for i in hit_num:
        pageRank[i] = hit_num[i] / n
    return pageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    #Calculate some constants from the corpus for further use:
    num_pages = len(corpus)
    init_rank = 1 / num_pages
    random_choice_prob = (1 - damping_factor) / len(corpus)
    iterations = 0

    # Initial page_rank gives every page a rank of 1/(num pages in corpus)
    page_ranks = {page_name: init_rank for page_name in corpus.keys()}
    new_ranks = {page_name: init_rank for page_name in corpus}
    max_rank_change = init_rank

    # Iteratively calculate page rank until no change > 0.001
    while max_rank_change > 0.001:
        # Update page ranks to the new ranks:
        page_ranks = new_ranks.copy()

        iterations += 1
        max_rank_change = 0

        for page_name in corpus:
            surf_choice_prob = 0
            for other_page in corpus:
                # If other page has no links it picks randomly any corpus page:
                if len(corpus[other_page]) == 0:
                    surf_choice_prob += page_ranks[other_page] * init_rank
                # Else if other_page has a link to page_name, it randomly picks from all links on other_page:
                elif page_name in corpus[other_page]:
                    surf_choice_prob += page_ranks[other_page] / len(corpus[other_page])
            # Calculate new page rank
            new_rank = random_choice_prob + (damping_factor * surf_choice_prob)
            new_ranks[page_name] = new_rank

        # Normalise the new page ranks:
        norm_factor = sum(new_ranks.values())
        new_ranks = {page: (rank / norm_factor) for page, rank in new_ranks.items()}

        # Find max change in page rank:
        for page_name in corpus:
            rank_change = abs(page_ranks[page_name] - new_ranks[page_name])
            if rank_change > max_rank_change:
                max_rank_change = rank_change


    print('Iteration took', iterations, 'iterations to converge')
    print('Sum of iteration page ranks: ', round(sum(page_ranks.values()), 4))

    return page_ranks



if __name__ == "__main__":
    main()