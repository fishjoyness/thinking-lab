#!/usr/bin/env python3
"""
思维实验室 - 每日概念自动更新脚本
在 GitHub Actions 上运行，每天往 index.html 里加 1-2 个新的心理学/经济学概念。
概念数据从 concepts.json 读取。
"""

import re
import json
import random
import datetime
import os

HTML_FILE = "index.html"
CONCEPTS_FILE = os.path.join(os.path.dirname(__file__), "concepts.json")


def load_concepts():
    with open(CONCEPTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def read_html():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read()


def get_existing_names(html):
    """提取已存在的概念名"""
    names = set(re.findall(r"<h3>(.+?)</h3>", html))
    return names


def generate_card(concept, section_type):
    """生成一张概念卡片的 HTML"""
    badge_class = "psych" if section_type == "psychology" else "econ"
    card = f"""    <div class="concept-card">
      <span class="badge {badge_class}">{concept["badge"]}</span>
      <h3>{concept["name"]}</h3>
      <div class="en">{concept["english"]}</div>
      <p>{concept["desc"]}</p>
      <div class="example">
        <span class="tag-label">生活</span><br>
        {concept["life"]}<br>
        <span class="tag-label">创业</span><br>
        {concept["entre"]}
      </div>
    </div>"""
    return card


def insert_into_section(html, section_id, new_cards_html):
    """在指定 section 的 card-grid 最后一张卡片后面插入新卡片"""
    # 匹配 section 内容直到最后的 </div>\n  </div>\n</section>
    pattern = rf'(<section id="{section_id}">[\s\S]*?)(\n  </div>\n</section>)'
    match = re.search(pattern, html)
    if not match:
        print(f"WARNING: 无法找到 section {section_id}")
        return html

    before = html[:match.end(1)]
    after = match.group(2) + html[match.end():]
    return before + "\n" + new_cards_html + after


def update_stats(html, psych_count, econ_count):
    """更新首页统计数字"""
    html = re.sub(
        r'(<div class="num psych">)\d+(</div>)',
        rf'\g<1>{psych_count}\g<2>',
        html
    )
    html = re.sub(
        r'(<div class="num econ">)\d+(</div>)',
        rf'\g<1>{econ_count}\g<2>',
        html
    )
    return html


def count_cards_in_section(html, section_id):
    """统计某个 section 里的概念卡片数量"""
    pattern = rf'<section id="{section_id}">[\s\S]*?</section>'
    match = re.search(pattern, html)
    if not match:
        return 0
    return len(re.findall(r'<div class="concept-card">', match.group(0)))


def main():
    data = load_concepts()
    html = read_html()
    existing = get_existing_names(html)

    # 筛选可添加的概念
    available_psych = [c for c in data["psychology"] if c["name"] not in existing]
    available_econ = [c for c in data["economics"] if c["name"] not in existing]

    if not available_psych and not available_econ:
        print("所有概念已添加完毕，没有新概念可加了。")
        return

    # 判断工作日/周末
    today = datetime.date.today()
    is_weekend = today.weekday() >= 5

    # 选 1-2 个概念
    num_to_add = random.randint(1, 2)
    added = []

    for _ in range(num_to_add):
        if is_weekend and available_psych:
            concept = random.choice(available_psych)
            available_psych.remove(concept)
            added.append(("psychology", concept))
        elif not is_weekend and available_econ:
            concept = random.choice(available_econ)
            available_econ.remove(concept)
            added.append(("economics", concept))
        elif available_psych:
            concept = random.choice(available_psych)
            available_psych.remove(concept)
            added.append(("psychology", concept))
        elif available_econ:
            concept = random.choice(available_econ)
            available_econ.remove(concept)
            added.append(("economics", concept))
        else:
            break

    if not added:
        print("没有新概念可加。")
        return

    # 按类型分组生成卡片
    psych_cards = []
    econ_cards = []
    for section_type, concept in added:
        card = generate_card(concept, section_type)
        if section_type == "psychology":
            psych_cards.append(card)
        else:
            econ_cards.append(card)

    # 插入到 HTML
    if psych_cards:
        html = insert_into_section(html, "psychology", "\n".join(psych_cards))
    if econ_cards:
        html = insert_into_section(html, "economics", "\n".join(econ_cards))

    # 统计当前数量
    psych_count = count_cards_in_section(html, "psychology")
    econ_count = count_cards_in_section(html, "economics")

    html = update_stats(html, psych_count, econ_count)

    # 写回文件
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    names = [c["name"] for _, c in added]
    print(f"添加了 {len(added)} 个概念: {', '.join(names)}")
    print(f"心理学概念总数: {psych_count}, 经济学概念总数: {econ_count}")
    print(f"剩余可用: 心理学 {len(available_psych)}, 经济学 {len(available_econ)}")


if __name__ == "__main__":
    main()
