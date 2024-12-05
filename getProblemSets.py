import requests

class CodeforcesFetcher:
    def __init__(self):
        self.api_url = "https://codeforces.com/api/problemset.problems"

    def fetch_problems(self, tags_include=None, rating_min=None, rating_max=None, include_only=False):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            if data["status"] != "OK":
                raise Exception("Failed to fetch problems")

            problems = data["result"]["problems"]
            filtered_problems = []

            for problem in problems:
                if "rating" in problem and problem["rating"] is not None:
                    if rating_min and problem["rating"] < rating_min:
                        continue
                    if rating_max and problem["rating"] > rating_max:
                        continue
                else:
                    continue

                if tags_include:
                    problem_tags = problem.get("tags", [])

                    if include_only:
                        if sorted(problem_tags) != sorted(tags_include):
                            continue
                    else:
                        if not any(tag in problem_tags for tag in tags_include):
                            continue

                filtered_problems.append({
                    "name": problem["name"],
                    "contestId": problem["contestId"],
                    "index": problem["index"],
                    "rating": problem["rating"],
                    "tags": problem.get("tags", [])
                })

            return filtered_problems

        except requests.exceptions.RequestException as e:
            return f"Network error: {e}"
        except Exception as e:
            return f"Error: {e}"
