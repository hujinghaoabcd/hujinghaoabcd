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
    readme_path = sys.argv[3]

    headers = {"Authorization": f"token {token}"}
    followers = []
    cursor = None

    while True:
        query = f'''
query {{
    user(login: "{handle}") {{
        followers(first: 10{f', after: "{cursor}"' if cursor else ''}) {{
            pageInfo {{
                endCursor
                hasNextPage
            }}
            nodes {{
                login
                name
                databaseId
                followers {{
                    totalCount
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
            print(response.status_code)
            print(response.text)
            raise SystemExit(1)

        result = response.json()["data"]["user"]["followers"]
        for follower in result["nodes"]:
            login = follower["login"]
            name = follower["name"] or login
            user_id = follower["databaseId"]
            follower_count = follower["followers"]["totalCount"]
            followers.append((follower_count, login, user_id, name))

        if not result["pageInfo"]["hasNextPage"]:
            break
        cursor = result["pageInfo"]["endCursor"]

    followers.sort(reverse=True)

    html = "<table>\n"
    for i, (_, login, user_id, name) in enumerate(followers[:32]):
        if i % 8 == 0:
            if i:
                html += "  </tr>\n"
            html += "  <tr>\n"

        html += f'''    <td align="center">
      <a href="https://github.com/{login}">
        <img src="https://avatars.githubusercontent.com/u/{user_id}?v=4&s=64" width="64" height="64" alt="{login}" />
      </a>
      <br />
      <sub><a href="https://github.com/{login}">{name}</a></sub>
    </td>
'''

    html += "  </tr>\n</table>"

    targets = [readme_path]
    if os.path.basename(readme_path) == "README.md":
        chinese_readme = os.path.join(os.path.dirname(readme_path), "README_CN.md")
        if os.path.exists(chinese_readme):
            targets.append(chinese_readme)

    for target in targets:
        update_readme(target, html)
        print(f"Updated followers in {target}")
