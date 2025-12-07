# Statistical Analysis of Cleaned Data

# This code will determine the following information:

# Most adopted cat breed, age, and sex and most adopted dog breed, age, and sex
# Most for adoption cat breed, age, and sex and least for adoption dog breed, age, and sex
# Least adopted cat breed, age, and sex and least adopted dog breed, age, and sex
# Least for adoption cat breed, age, and sex and least for adoption dog breed, age, and sex

# Bar plots of adopted cats and dogs based on number of each breed, age
# Bar plots of for adoption cats and dogs based on number of each breed, age

# Chi-squared tests to check for dependency between categorical variables
# Does the breed, sex, or age impact adoptive status?

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from scipy import stats

# Perform chi-squared test on a particular category, comparing adopted vs for adoption
def chi_square_test(df_adopted, df_not, column):
    # Performs chi-square test on a categorical variable (e.g., age, sex, or breed).
    combined = pd.concat([df_adopted, df_not], ignore_index=True)

    contingency = pd.crosstab(combined[column], combined['Adopted'])

    chi2, p, dof, expected = stats.chi2_contingency(contingency)

    return {
        "contingency_table": contingency,
        "chi2": chi2,
        "p_value": p,
        "degrees_of_freedom": dof,
        "expected": expected
    }

def plot_split_bar(contingency, title, xlabel="Category"):
    # Produces two separate bar charts:
    # - left: not adopted
    # - right: adopted
    # contingency: DataFrame (rows = categories, columns = [not adopted, adopted])

    categories = contingency.index
    not_adopted = contingency["No"] if "No" in contingency.columns else None
    adopted = contingency["Yes"] if "Yes" in contingency.columns else None

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left plot — not adopted
    axes[0].bar(categories, not_adopted)
    axes[0].set_title("Not Adopted")
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylabel("Count")
    axes[0].tick_params(axis='x', rotation=45)

    # Right plot — adopted
    axes[1].bar(categories, adopted)
    axes[1].set_title("Adopted")
    axes[1].set_xlabel(xlabel)
    axes[1].tick_params(axis='x', rotation=45)

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

def plot_horizontal_bars(contingency, title, xlabel="Count"):
    # Creates two horizontal bar plots stacked vertically:
    # top = not adopted
    # bottom = adopted
    # Each subplot has its own x-axis scale.

    categories = contingency.index
    not_adopted = contingency["No"] if "No" in contingency.columns else None
    adopted = contingency["Yes"] if "Yes" in contingency.columns else None

    # Auto-adjust figure height based on number of categories
    height = max(6, len(categories) * 0.4)
    fig, axes = plt.subplots(2, 1, figsize=(10, height), sharex=False)

    # --- Top plot (Not Adopted) ---
    axes[0].barh(categories, not_adopted)
    axes[0].set_title("Not Adopted")
    axes[0].set_xlabel(xlabel)
    axes[0].invert_yaxis()   # So categories appear in same order as bottom
    axes[0].grid(axis='x', linestyle='--', alpha=0.5)

    # --- Bottom plot (Adopted) ---
    axes[1].barh(categories, adopted)
    axes[1].set_title("Adopted")
    axes[1].set_xlabel(xlabel)
    axes[1].invert_yaxis()
    axes[1].grid(axis='x', linestyle='--', alpha=0.5)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

def plot_age_sex(df_adopted, df_not, title, column):
    combined = pd.concat([df_adopted, df_not], ignore_index=True)
    contingency = pd.crosstab(combined[column], combined['Adopted'])
    plot_split_bar(contingency, title)

def plot_breed_distribution(df_adopted, df_not, title, min_count=100):
    combined = pd.concat([df_adopted, df_not], ignore_index=True)

    # count total occurrences per breed
    breed_counts = combined['Breed'].value_counts()

    # filter to breeds with > min_count total entries
    allowed_breeds = breed_counts[breed_counts > min_count].index

    filtered = combined[combined['Breed'].isin(allowed_breeds)]

    # if nothing passes the filter, skip
    if filtered.empty:
        print(f"No breeds with more than {min_count} animals. Skipping plot.")
        return

    contingency = pd.crosstab(filtered['Breed'], filtered['Adopted'])

    plot_horizontal_bars(contingency, title)

def find_minmax(dframe):
    # count total occurrences per category
    breed_counts = dframe['Breed'].value_counts()
    age_counts = dframe["Age"].value_counts()
    sex_counts = dframe["Gender"].value_counts()

    # Find maximums
    max_breed = breed_counts.index[0]
    max_age = age_counts.index[0]
    max_sex = sex_counts.index[0]

    # Find minimuns (note - min_breed is a list of all the breeds with only 1)
    min_breed = list(breed_counts[breed_counts == 1].index)
    min_age = age_counts.index[-1]
    min_sex = sex_counts.index[1]

    return max_breed, max_age, max_sex, min_breed, min_age, min_sex

def main():

    cats_adopted = pd.read_csv("cleanedData/petDatacats-adopte-CLEANED.csv")
    cats_adopted["Adopted"] = "Yes"
    cats_for_adop = pd.read_csv("cleanedData/petDatacats-for-ad-CLEANED.csv")
    cats_for_adop["Adopted"] = "No"

    dogs_adopted = pd.read_csv("cleanedData/petDatadogs-adopte-CLEANED.csv")
    dogs_adopted["Adopted"] = "Yes"
    dogs_for_adop = pd.read_csv("cleanedData/petDatadogs-for-ad-CLEANED.csv")
    dogs_for_adop["Adopted"] = "No"

    # Run chi-squared tests
    cats_age_results = chi_square_test(cats_adopted, cats_for_adop, "Age")
    dogs_age_results = chi_square_test(dogs_adopted, dogs_for_adop, "Age")
    cats_sex_results = chi_square_test(cats_adopted, cats_for_adop, "Gender")
    dogs_sex_results = chi_square_test(dogs_adopted, dogs_for_adop, "Gender")
    cats_breed_results = chi_square_test(cats_adopted, cats_for_adop, "Breed")
    dogs_breed_results = chi_square_test(dogs_adopted, dogs_for_adop, "Breed")

    # Determine max and min
    cats_adopted_minmax = find_minmax(cats_adopted)
    cats_for_adop_minmax = find_minmax(cats_for_adop)
    dogs_adopted_minmax = find_minmax(dogs_adopted)
    dogs_for_adop_minmax = find_minmax(dogs_for_adop)
    
    # Plot data about the genders and ages
    plot_age_sex(cats_adopted, cats_for_adop, "Cats Adopted/For Adoption by Gender", "Gender")
    plot_age_sex(cats_adopted, cats_for_adop, "Cats Adopted/For Adoption by Age", "Age")
    plot_age_sex(dogs_adopted, dogs_for_adop, "Dogs Adopted/For Adoption by Gender", "Gender")
    plot_age_sex(dogs_adopted, dogs_for_adop, "Dogs Adopted/For Adoption by Age", "Age")

    # To plot the data about breeds, remove any breed with less than 100
    plot_breed_distribution(cats_adopted, cats_for_adop, "Cats Adopted/For Adoption by Breed")
    plot_breed_distribution(dogs_adopted, dogs_for_adop, "Dogs Adopted/For Adoption by Breed")
    
    # Store chi-squared test and min/max data
    output = open("./outputData/analysisOutput.txt", "w")
    output.write(
        f"""Chi-Squared Test Results and Min/Max Data

        Chi-Squared Tests:
        Cats:
        Age Results:
        {cats_age_results}
        Gender Results:
        {cats_sex_results}
        Breed Results:
        {cats_breed_results}

        Dogs:
        Age Results:
        {dogs_age_results}
        Gender Results:
        {dogs_sex_results}
        Breed Results:
        {dogs_breed_results}

        Min/Max Data:

        Cats:
        Adopted:
        Max Breed: {cats_adopted_minmax[0]}
        Min Breeds: {cats_adopted_minmax[3]}
        Max Age: {cats_adopted_minmax[1]}
        Min Age: {cats_adopted_minmax[4]}
        Max Gender: {cats_adopted_minmax[2]}
        Min Gender: {cats_adopted_minmax[5]}

        For Adoption:
        Max Breed: {cats_for_adop_minmax[0]}
        Min Breeds: {cats_for_adop_minmax[3]}
        Max Age: {cats_for_adop_minmax[1]}
        Min Age: {cats_for_adop_minmax[4]}
        Max Gender: {cats_for_adop_minmax[2]}
        Min Gender: {cats_for_adop_minmax[5]}

        Dogs:
        Adopted:
        Max Breed: {dogs_adopted_minmax[0]}
        Min Breeds: {dogs_adopted_minmax[3]}
        Max Age: {dogs_adopted_minmax[1]}
        Min Age: {dogs_adopted_minmax[4]}
        Max Gender: {dogs_adopted_minmax[2]}
        Min Gender: {dogs_adopted_minmax[5]}

        For Adoption:
        Max Breed: {dogs_for_adop_minmax[0]}
        Min Breeds: {dogs_for_adop_minmax[3]}
        Max Age: {dogs_for_adop_minmax[1]}
        Min Age: {dogs_for_adop_minmax[4]}
        Max Gender: {dogs_for_adop_minmax[2]}
        Min Gender: {dogs_for_adop_minmax[5]}
        """
    )

    output.close()
    return
main()