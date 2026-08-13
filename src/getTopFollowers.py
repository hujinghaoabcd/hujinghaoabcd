import requests
import json
import sys
import re
import os


def update_readme(path, html):
    with open(path, "r", encoding="utf-8") as readme:
        content = readme.read()

    new_content = re.sub(
        r"(?<=<!\-\-START_SECTION:top\-followers\-\->)[\s\S]*(?=<!\-\-END_SECTION:top\-followers\-\->)",
        f"\n{html}\n",
        content,
    )

    with open(path, "w", encoding="utf-8") as readme:
        readme.write(new_content)


if __name__ == "__main__":
    assert len(sys.argv) == 4
    handle = sys.argv[1]
    token = sys.argv[2]
    readmePath = sys.argv[3]

    headers = {
        "Authorization": f"token {token}"
    }

    followers = []
    cursor = None

    while True:
        query = f'''
query {{
    user(login: "{handle}") {{
        followers(first: 10{f', after: "{cursor}"' if cursor else ''}) {{
            pageInfo{{
                endCursor
                hasNextPage
            }}
            nodes {{
                login
                name
                databaseId
                following {{
                    totalCount
                }}
                repositories(first: 3, isFork: false, orderBy: {{
                    field: STARGAZERS,
                    direction: DESC
                }}) {{
                    totalCount
                    nodes {{
                        stargazerCount
                    }}
                }}
                followers {{
                    totalCount
                }}
                contributionsCollection {{
                    contributionCalendar {{
                        totalContributions
                    }}
                }}
            }}
        }}
    }}
}}
'''
        response = requests.post(
            "https://api.github.com/graphql",
            json.dumps({"query": query}),
            headers=headers,
        )
        if not response.ok or "data" not in response.json():
            print(query)
            print(response.status_code)
            print(response.text)
            exit(1)

        res = response.json()["data"]["user"]["followers"]
        for follower in res["nodes"]:
            repo_count = follower["repositories"]["totalCount"]
            login = follower["login"]
            name = follower["name"]
            user_id = follower["databaseId"]
            follower_number = follower["followers"]["totalCount"]
            followers.append(
                (follower_number, login, user_id, name if name else login)
            )
            print(followers[-1])

        sys.stdout.flush()
        if not res["pageInfo"]["hasNextPage"]:
            break
        cursor = res["pageInfo"]["endCursor"]

    followers.sort(reverse=True)

    html = "<table>\n"

    for i in range(min(len(followers), 32)):
        login = followers[i][1]
        user_id = followers[i][2]
        name = followers[i][3]
        if i % 8 == 0:
            if i != 0:
                html += "  </tr>\n"
            html += "  <tr>\n"
        html += f'''    <td align="center">
      <a href="https://github.com/{login}">
        <img src="https://avatars2.githubusercontent.com/u/{user_id}" width="64px;" alt="{login}"/>
      </a>
      <br />
      <sub><a href="https://github.com/{login}">{name}</a></sub>
    </td>
'''

    html += "  </tr>\n</table>"

    targets = [readmePath]
    if os.path.basename(readmePath) == "README.md":
        chinese_readme = os.path.join(os.path.dirname(readmePath), "README_CN.md")
        if os.path.exists(chinese_readme):
            targets.append(chinese_readme)

    for target in targets:
        update_readme(target, html)
        print(f"Updated followers in {target}")
