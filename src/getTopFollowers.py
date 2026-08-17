import requests
import json
import sys
import re
import os


SKILLS_WALL = '''<p>
  <kbd>Python</kbd> <kbd>R</kbd> <kbd>C++</kbd> <kbd>JavaScript</kbd> <kbd>TypeScript</kbd> <kbd>SQL / PostgreSQL</kbd> <kbd>Bash</kbd> <kbd>PowerShell</kbd>
  <br/>
  <kbd>HTML5</kbd> <kbd>CSS3</kbd> <kbd>Markdown</kbd> <kbd>LaTeX</kbd> <kbd>PyTorch</kbd> <kbd>NumPy</kbd> <kbd>SciPy</kbd> <kbd>Pandas</kbd> <kbd>scikit-learn</kbd> <kbd>Jupyter</kbd> <kbd>Matplotlib</kbd> <kbd>Plotly</kbd>
  <br/>
  <kbd>GeoPandas</kbd> <kbd>QGIS</kbd> <kbd>PostGIS</kbd> <kbd>GDAL</kbd> <kbd>MapLibre</kbd> <kbd>Leaflet</kbd> <kbd>OpenLayers</kbd>
  <br/>
  <kbd>Vue</kbd> <kbd>React</kbd> <kbd>Django</kbd> <kbd>Node.js</kbd> <kbd>Vite</kbd> <kbd>pnpm</kbd> <kbd>SQLite</kbd> <kbd>Git</kbd> <kbd>GitHub</kbd> <kbd>Docker</kbd> <kbd>Linux</kbd> <kbd>CMake</kbd> <kbd>Qt</kbd> <kbd>Sphinx</kbd> <kbd>GitHub Actions</kbd> <kbd>VS Code</kbd>
</p>'''

FEATURED_EN = '''| Project | Project |
| --- | --- |
| **[spatialshap](https://github.com/hujinghaoabcd/spatialshap)**<br/><sub>Spatially conditioned Shapley explanations for geospatial models.</sub> | **[DH-STGCN](https://github.com/hujinghaoabcd/DH-STGCN)**<br/><sub>Dynamic hierarchical spatiotemporal graph learning for traffic forecasting.</sub> |
| **[pyGeoHet](https://github.com/hujinghaoabcd/pyGeoHet)**<br/><sub>Spatially stratified heterogeneity analysis and GeoDetector methods.</sub> | **[pySTARMAx](https://github.com/hujinghaoabcd/pySTARMAx)**<br/><sub>STARMA / STARIMA modeling for spatiotemporal data.</sub> |
| **[pyKDEX](https://github.com/hujinghaoabcd/pyKDEX)**<br/><sub>Kernel-density and geospatial analysis workflows in Python.</sub> | **[pySurveying](https://github.com/hujinghaoabcd/pySurveying)**<br/><sub>Surveying computation, adjustment, QC and visualization.</sub> |
| **[soil_interpolation](https://github.com/hujinghaoabcd/soil_interpolation)**<br/><sub>Geostatistical workflows for soil spatial interpolation.</sub> | **[GeoPortalX](https://github.com/hujinghaoabcd/GeoPortalX)**<br/><sub>Lightweight geospatial data portal and web mapping platform.</sub> |
| **[OMap](https://github.com/hujinghaoabcd/openlayers-webgis-platform)**<br/><sub>Modular OpenLayers / Vue / TypeScript WebGIS framework.</sub> | **[AirSimPortal](https://github.com/hujinghaoabcd/AirSimPortal)**<br/><sub>Atmospheric dispersion simulation and geospatial data platform.</sub> |
| **[ZhiDun](https://github.com/hujinghaoabcd/zhidun-crime-analysis)**<br/><sub>GIS-oriented crime spatiotemporal analysis and visualization.</sub> | **[StarHub](https://github.com/hujinghaoabcd/StarHub)**<br/><sub>GitHub repository and project management utilities.</sub> |
| **[RepoForge](https://github.com/hujinghaoabcd/RepoForge)**<br/><sub>Repository scaffolding and standardization tooling.</sub> | **[PlotLibre](https://github.com/hujinghaoabcd/PlotLibre)**<br/><sub>MapLibre-native semantic parametric plotting framework.</sub> |'''

FEATURED_CN = '''| 项目 | 项目 |
| --- | --- |
| **[spatialshap](https://github.com/hujinghaoabcd/spatialshap)**<br/><sub>面向地理空间模型的空间条件 Shapley 可解释分析。</sub> | **[DH-STGCN](https://github.com/hujinghaoabcd/DH-STGCN)**<br/><sub>面向交通预测的动态层次时空图学习模型。</sub> |
| **[pyGeoHet](https://github.com/hujinghaoabcd/pyGeoHet)**<br/><sub>空间分层异质性与 GeoDetector 分析工具。</sub> | **[pySTARMAx](https://github.com/hujinghaoabcd/pySTARMAx)**<br/><sub>面向时空数据的 STARMA / STARIMA 建模工具。</sub> |
| **[pyKDEX](https://github.com/hujinghaoabcd/pyKDEX)**<br/><sub>Python 核密度与地理空间分析工作流。</sub> | **[pySurveying](https://github.com/hujinghaoabcd/pySurveying)**<br/><sub>测量计算、平差、质控与可视化工具。</sub> |
| **[soil_interpolation](https://github.com/hujinghaoabcd/soil_interpolation)**<br/><sub>土壤空间插值与地统计分析工作流。</sub> | **[GeoPortalX](https://github.com/hujinghaoabcd/GeoPortalX)**<br/><sub>轻量级地理空间数据门户与 Web 地图平台。</sub> |
| **[OMap](https://github.com/hujinghaoabcd/openlayers-webgis-platform)**<br/><sub>基于 OpenLayers / Vue / TypeScript 的模块化 WebGIS 框架。</sub> | **[AirSimPortal](https://github.com/hujinghaoabcd/AirSimPortal)**<br/><sub>大气污染扩散模拟与地理空间数据平台。</sub> |
| **[ZhiDun](https://github.com/hujinghaoabcd/zhidun-crime-analysis)**<br/><sub>面向 GIS 的犯罪时空分析与可视化系统。</sub> | **[StarHub](https://github.com/hujinghaoabcd/StarHub)**<br/><sub>GitHub 仓库与项目管理工具。</sub> |
| **[RepoForge](https://github.com/hujinghaoabcd/RepoForge)**<br/><sub>仓库脚手架与规范化工具。</sub> | **[PlotLibre](https://github.com/hujinghaoabcd/PlotLibre)**<br/><sub>MapLibre 原生语义化参数绘图框架。</sub> |'''


def stabilize_static_sections(path):
    with open(path, "r", encoding="utf-8") as readme:
        content = readme.read()

    is_cn = os.path.basename(path) == "README_CN.md"
    banner_alt = "科技像素风头图" if is_cn else "Pixel technology banner"
    banner = f'''<p align="center">
  <a href="https://github.com/hujinghaoabcd">
    <img src="assets/profile-banner-pixel.png" width="100%" alt="{banner_alt}" />
  </a>
</p>'''

    # Everything before the main animated heading is only the banner area.
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
            lambda m: m.group(1) + FEATURED_CN + m.group(2),
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
            lambda m: m.group(1) + FEATURED_EN + m.group(2),
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
        print(f"Updated stable profile sections in {target}")
