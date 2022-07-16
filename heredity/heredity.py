import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    # i.e. the probability if we know nothing about that person's parent
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait *given* two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")

    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    # dict contain a dict of person which contain a dict of two keys, gene and trait which are also the dict
    probabilities = {
        person: {  # a string
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_p = 1
    # set of people who has no parent
    people_with_parent = set()
    # set of people who has parents in people
    people_without_parent = set()

    # classify them
    for person, per in people.items():
        if per["mother"] is None:  # belong to no parent
            people_without_parent.add(person)  # add string type to it
        else:
            people_with_parent.add(person)

    # final goal, joint_prob = p(one_gene) * p(two_gene) * p(does not have gene) * p(has trait) * p(do not have trait)

    # *for those who have no parent* #
    p_wo_parent = 1

    # for those in both one_gene and has trait probability:

    set1_1 = one_gene.intersection(have_trait)

    # for those in both one_gene and has no trait

    set1_2 = one_gene - set1_1

    # for those in both two_gene and has trait

    set2_1 = two_genes.intersection(have_trait)

    # for those in both one_gene and has no trait

    set2_2 = two_genes - set2_1

    # for those in both no_gene and has trait

    set0 = (set(people.keys()) - one_gene) - two_genes
    set0_1 = set0.intersection(have_trait)

    # for those in both no_gene and has no trait

    set0_2 = set0 - set0_1

    # create a dict which store the possibility of parent passing its gene to children
    prob_pass = dict()

    for person in people_without_parent:
        # 1 gene & trait
        if person in set1_1:
            p_wo_parent *= (PROBS["gene"][1] * PROBS["trait"][1][True])
            prob_pass[person] = 0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])
        elif person in set1_2:
            p_wo_parent *= (PROBS["gene"][1] * PROBS["trait"][1][False])
            prob_pass[person] = 0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])
        elif person in set2_1:
            p_wo_parent *= (PROBS["gene"][2] * PROBS["trait"][2][True])
            prob_pass[person] = 1 - PROBS["mutation"]
        elif person in set2_2:
            p_wo_parent *= (PROBS["gene"][2] * PROBS["trait"][2][False])
            prob_pass[person] = 1 - PROBS["mutation"]
        elif person in set0_1:
            p_wo_parent *= (PROBS["gene"][0] * PROBS["trait"][0][True])
            prob_pass[person] = PROBS["mutation"]
        elif person in set0_2:
            p_wo_parent *= (PROBS["gene"][0] * PROBS["trait"][0][False])
            prob_pass[person] = PROBS["mutation"]

    # probability combined with people with parent

    p_w_parent = 1
    for person in people_with_parent:
        mother = people[person]["mother"]
        father = people[person]["father"]
        if person in set0:  # calculate the probs of no gene passing
            pp = ((1 - prob_pass[mother]) * (1 - prob_pass[father]))
            if person in have_trait:
                p_w_parent *= pp * (PROBS["trait"][0][True])
            else:
                p_w_parent *= pp * (PROBS["trait"][0][False])
        elif person in one_gene:  # calculate either father passing or mother passing
            pass_by_mom = prob_pass[mother] * (1 - prob_pass[father])
            pass_by_father = prob_pass[father] * (1 - prob_pass[mother])
            pp = (pass_by_mom + pass_by_father)
            if person in have_trait:
                p_w_parent *= pp * (PROBS["trait"][1][True])
            else:
                p_w_parent *= pp * (PROBS["trait"][1][False])
        elif person in two_genes:
            pp = (prob_pass[mother] * prob_pass[father])
            if person in have_trait:
                p_w_parent *= pp * (PROBS["trait"][2][True])
            else:
                p_w_parent *= pp * (PROBS["trait"][2][False])

    return p_w_parent * p_wo_parent


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # update each person per cycle
    for person in probabilities:
        num_gene = (2 if person in two_genes else 1 if person in one_gene else 0)
        trait = person in have_trait

        # update to current probability (as all combo of variable will be added up)
        probabilities[person]['gene'][num_gene] += p
        probabilities[person]['trait'][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:  # person is key, not dictionary itself, which means, person is a string type
        # for each person, gene section add up to 1; trait section add up to 1

        factor_1 = sum(probabilities[person]['gene'].values())
        factor_2 = sum(probabilities[person]['trait'].values())

        factor_1 = 1/factor_1
        factor_2 = 1/factor_2

        # normalize gene
        for x, y in probabilities[person]['gene'].items():
            probabilities[person]['gene'][x] = y * factor_1

        print(probabilities[person]['trait'])
        # normalize trait
        probabilities[person]['trait'][True] *= factor_2
        probabilities[person]['trait'][False] *= factor_2


if __name__ == "__main__":
    main()
