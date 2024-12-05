import streamlit as st
from getProblemSets import CodeforcesFetcher
import const
import random

fetcher = CodeforcesFetcher()

st.set_page_config(page_title="Codeforces Problem Finder", layout="centered")

st.title("🎯 Codeforces Problem Finder")
st.write("Find Codeforces problems based on tags, rating, and other preferences.")

tags = const.tags

with st.sidebar:
    st.header("Filter Options")
    include_tags = st.multiselect(
        "Select Tags",
        options=tags,
    )
    
    min_rating = st.number_input("Minimum Rating", min_value=800, max_value=3500, step=100, value=800)
    max_rating = st.number_input("Maximum Rating", min_value=800, max_value=3500, step=100, value=1200)
    include_only = st.checkbox("Include Tags Only", value=False)
    show_count = st.slider("Number of Problems to Display", min_value=1, max_value=50, value=10)
    fetch_problems = st.button("Fetch Problems")

if fetch_problems:
    problems = fetcher.fetch_problems(
        tags_include=include_tags,
        rating_min=min_rating,
        rating_max=max_rating,
        include_only=include_only
    )

    if isinstance(problems, str):
        st.error(problems)
    elif problems:
        st.success(f"Found {len(problems)} problems!")
        random_problems = random.sample(problems, min(show_count, len(problems)))

        for i, problem in enumerate(random_problems, start=1):
            st.markdown(f"### {i}. {problem['name']}")
            st.write(f"**Rating**: {problem['rating']}")
            st.write(f"**Tags**: {', '.join(problem['tags'])}")
            st.write(f"[View Problem](https://codeforces.com/contest/{problem['contestId']}/problem/{problem['index']})")
    else:
        st.warning("No problems found with the selected filters.")
