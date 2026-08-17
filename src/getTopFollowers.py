import requests
import json
import sys
import re
import os


SKILLS_WALL = '''<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/R-276DC3?style=flat-square&logo=r&logoColor=white" alt="R" />
  <img src="https://img.shields.io/badge/C++-00599C?style=flat-square&logo=cplusplus&logoColor=white" alt="C++" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=000" alt="JavaScript" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white" alt="Bash" />
  <img src="https://img.shields.io/badge/PowerShell-5391FE?style=flat-square&logo=powershell&logoColor=white" alt="PowerShell" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-663399?style=flat-square&logo=css&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/Markdown-000000?style=flat-square&logo=markdown&logoColor=white" alt="Markdown" />
  <img src="https://img.shields.io/badge/LaTeX-008080?style=flat-square&logo=latex&logoColor=white" alt="LaTeX" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" alt="NumPy" />
  <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white" alt="SciPy" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white" alt="Jupyter" />
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logo=python&logoColor=white" alt="Matplotlib" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/GeoPandas-139C5A?style=flat-square&logo=geopandas&logoColor=white" alt="GeoPandas" />
  <img src="https://img.shields.io/badge/QGIS-589632?style=flat-square&logo=qgis&logoColor=white" alt="QGIS" />
  <img src="https://img.shields.io/badge/PostGIS-336791?style=flat-square&logo=postgresql&logoColor=white" alt="PostGIS" />
  <img src="https://img.shields.io/badge/GDAL-5CAE58?style=flat-square&logo=gdal&logoColor=white" alt="GDAL" />
  <img src="https://img.shields.io/badge/MapLibre-396CB2?style=flat-square&logo=maplibre&logoColor=white" alt="MapLibre" />
  <img src="https://img.shields.io/badge/Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white" alt="Leaflet" />
  <img src="https://img.shields.io/badge/OpenLayers-1F6B75?style=flat-square&logo=openlayers&logoColor=white" alt="OpenLayers" />
  <img src="https://img.shields.io/badge/Vue-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" alt="Vue" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=000" alt="React" />
  <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Node.js-5FA04E?style=flat-square&logo=nodedotjs&logoColor=white" alt="Node.js" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/pnpm-F69220?style=flat-square&logo=pnpm&logoColor=white" alt="pnpm" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" alt="Git" />
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=000" alt="Linux" />
  <img src="https://img.shields.io/badge/CMake-064F8C?style=flat-square&logo=cmake&logoColor=white" alt="CMake" />
  <img src="https://img.shields.io/badge/Qt-41CD52?style=flat-square&logo=qt&logoColor=white" alt="Qt" />
  <img src="https://img.shields.io/badge/Sphinx-000000?style=flat-square&logo=sphinx&logoColor=white" alt="Sphinx" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/VS_Code-007ACC?style=flat-square&logo=visualstudiocode&logoColor=white" alt="VS Code" />
</p>'''

FEATURED_SVG = '''<p align="center">
  <a href="https://github.com/hujinghaoabcd/spatialshap"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/spatialshap.svg" width="49%" alt="spatialshap" /></a>
  <a href="https://github.com/hujinghaoabcd/DH-STGCN"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/dh-stgcn.svg" width="49%" alt="DH-STGCN" /></a>
  <br/>
  <a href="https://github.com/hujinghaoabcd/pyGeoHet"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/pygeohet.svg" width="49%" alt="pyGeoHet" /></a>
  <a href="https://github.com/hujinghaoabcd/pySTARMAx"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/pystarmax.svg" width="49%" alt="pySTARMAx" /></a>
  <br/>
  <a href="https://github.com/hujinghaoabcd/pyKDEX"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/pykdex.svg" width="49%" alt="pyKDEX" /></a>
  <a href="https://github.com/hujinghaoabcd/pySurveying"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/pysurveying.svg" width="49%" alt="pySurveying" /></a>
  <br/>
  <a href="https://github.com/hujinghaoabcd/soil_interpolation"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/soil-interpolation.svg" width="49%" alt="soil_interpolation" /></a>
  <a href="https://github.com/hujinghaoabcd/GeoPortalX"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/geoportalx.svg" width="49%" alt="GeoPortalX" /></a>
  <br/>
  <a href="https://github.com/hujinghaoabcd/openlayers-webgis-platform"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/openlayers-webgis-platform.svg" width="49%" alt="OMap" /></a>
  <a href="https://github.com/hujinghaoabcd/AirSimPortal"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/airsimportal.svg" width="49%" alt="AirSimPortal" /></a>
  <br/>
  <a href="https://github.com/hujinghaoabcd/zhidun-crime-analysis"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/zhidun-crime-analysis.svg" width="49%" alt="ZhiDun" /></a>
  <a href="https://github.com/hujinghaoabcd/StarHub"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/starhub.svg" width="49%" alt="StarHub" /></a>
  <br/>
  <a href="https://github.com/hujinghaoabcd/RepoForge"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/repoforge.svg" width="49%" alt="RepoForge" /></a>
  <a href="https://github.com/hujinghaoabcd/PlotLibre"><img src="https://cdn.jsdelivr.net/gh/hujinghaoabcd/hujinghaoabcd@master/assets/pinned/plotlibre.svg" width="49%" alt="PlotLibre" /></a>
</p>'''


def stabilize_static_sections(path):
    with open(path, "r", encoding="utf-8") as readme:
        content = readme.read()

    is_cn = os.path.basename(path) == "README_CN.md"
    banner_alt = "科技像素风头图" if is_cn else "Pixel technology banner"
    banner = f'''<p>
  <a href="https://github.com/hujinghaoabcd">
    <img src="assets/profile-banner-pixel.png" width="100%" alt="{banner_alt}" />
  </a>
</p>'''

    content = re.sub(
        r"\A[\s\S]*?(?=<h1 align=\"center\">)",
        banner + "\n\n",
        content,
        count=1,
    )

    if is_cn:
        content = re.sub(
            r"(## 🧰 语言、框架、工具和技能\n\n)[\s\S]*?(\n---\n\n## 🧭 研究与开源生态系统)",
            lambda m: m.group(1) + SKILLS_WALL + m.group(2),
            content,
            count=1,
        )
        content = re.sub(
            r"(## 🚀 精选项目\n\n)[\s\S]*?(\n---\n\n## 📚 文档与学习资源)",
            lambda m: m.group(1) + FEATURED_SVG + m.group(2),
            content,
            count=1,
        )
    else:
        content = re.sub(
            r"(## 🧰 Languages, Frameworks, Tools & Skills\n\n)[\s\S]*?(\n---\n\n## 🧭 Research & Open-source Ecosystem)",
            lambda m: m.group(1) + SKILLS_WALL + m.group(2),
            content,
            count=1,
        )
        content = re.sub(
            r"(## 🚀 Featured Projects\n\n)[\s\S]*?(\n---\n\n## 📚 Documentation & Learning)",
            lambda m: m.group(1) + FEATURED_SVG + m.group(2),
            content,
            count=1,
        )

    with open(path, "w", encoding="utf-8") as readme:
        readme.write(content)


def update_followers(path, html):
    with open(path, "r", encoding="utf-8") as readme:
        content = readme.read()

    content = re.sub(
        r"(?<=<!\-\-START_SECTION:top\-followers\-\->)[\s\S]*(?=<!\-\-END_SECTION:top\-followers\-\->)",
        f"\n{html}\n",
        content,
    )

    with open(path, "w", encoding="utf-8") as readme:
        readme.write(content)


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
        stabilize_static_sections(target)
        update_followers(target, html)
        print(f"Updated SVG profile sections in {target}")
