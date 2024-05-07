---
tod: false
theme: dashboard
title: 서울대 버스 네트워크
---

<style>
  @import url("https://fonts.googleapis.com/css?family=Noto+Serif+KR&display=swap");
  body {
    font-family: "Noto Serif KR", serif;
  }
</style>

# 서울대에는 어떤 버스들이 다닐까?🚌

### 지선버스

5513번, 5516번, 5511번 총 세대의 버스

### 간선버스와 마을버스

관악02 와 501번 총 두 대의 버스

### 셔틀버스

교내순환1, 교내순환 2 그 외 5대 이상의 셔틀버스들

### 서울대학교 정류장 그룹화

서울대학교의 정류장들은 그룹화가 가능합니다.
크게 윗 공대, 아랫 공대, 정문, 사회대, 자연대, 농생대, 경영대, 음대, 그리고 후문으로 나눌 수 있습니다.
그리고 이를 네트워크화 시키면 아래와 같은 네트워크를 얻을 수 있습니다.

---

```js
const width = 1000;
const height = 800;
const color = d3.scaleOrdinal(d3.schemeCategory10);

// 각 버스 노선에 따른 정류장 정보
const buses = {
  5513: [
    "경영대",
    "정문",
    "수의대",
    "음대",
    "사범대",
    "아랫공대",
    "윗공대",
    "농생대",
    "자연대",
  ],
  5516: [
    "정문",
    "경영대",
    "수의대",
    "자연대",
    "농생대",
    "윗공대",
    "아랫공대",
    "사범대",
    "음대",
  ],
  5511: [
    "정문",
    "경영대",
    "수의대",
    "음대",
    "사범대",
    "아랫공대",
    "윗공대",
    "농생대",
    "자연대",
  ],
  관악02: ["후문", "사범대", "윗공대", "아랫공대"],
  교내순환1: ["정문", "농생대", "아랫공대"],
  교내순환2: ["정문", "경영대", "후문", "윗공대"],
};

// 노드와 링크 생성
// 데이터 생성 로직 변경
const nodes = [],
  links = [];
const busStopsGroups = {
  경영대: 1,
  정문: 2,
  수의대: 3,
  음대: 4,
  사범대: 5,
  아랫공대: 6,
  윗공대: 7,
  농생대: 8,
  자연대: 9,
  후문: 10,
};

// 버스 데이터를 바탕으로 노드와 링크 생성
for (const bus in buses) {
  nodes.push({ id: bus, group: 0 }); // 버스를 그룹 0으로 설정
  buses[bus].forEach((stop) => {
    // 정류장 노드가 존재하지 않으면 추가
    if (!nodes.some((n) => n.id === stop)) {
      nodes.push({ id: stop, group: busStopsGroups[stop] || 0 });
    }
    links.push({ source: bus, target: stop, value: 1 }); // 버스와 정류장 연결
  });
}

// 연결 갯수에 따른 노드 크기 계산
const countLinks = {};
links.forEach((link) => {
  if (!countLinks[link.source]) countLinks[link.source] = 0;
  if (!countLinks[link.target]) countLinks[link.target] = 0;
  countLinks[link.source]++;
  countLinks[link.target]++;
});

// D3 시뮬레이션 설정
const simulation = d3
  .forceSimulation(nodes)
  .force(
    "link",
    d3
      .forceLink(links)
      .id((d) => d.id)
      .distance(50)
  )
  .force("charge", d3.forceManyBody().strength(-500))
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("collide", d3.forceCollide(50))
  .on("tick", ticked);

const svg = d3
  .create("svg")
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [0, 0, width, height])
  .style("max-width", "100%")
  .style("height", "auto");

const link = svg
  .append("g")
  .attr("stroke", "#999")
  .attr("stroke-opacity", 0.6)
  .selectAll("line")
  .data(links)
  .join("line")
  .attr("stroke-width", (d) => Math.sqrt(d.value));
// 시각화 코드 변경
const node = svg
  .append("g")
  .selectAll("circle")
  .data(nodes)
  .join("circle")
  .attr("r", (d) => 5 + Math.sqrt(countLinks[d.id] || 0) * 2) // 연결 수에 따른 반지름 설정
  .attr("fill", (d) => color(d.group))
  .call(drag(simulation));

const labels = svg
  .append("g")
  .attr("class", "labels")
  .selectAll("text")
  .data(nodes)
  .join("text")
  .attr("x", (d) => d.x)
  .attr("y", (d) => d.y)
  .text((d) => d.id) // 텍스트는 노드 ID로 설정
  .style("font-size", "12px")
  .style("fill", "#333")
  .style("font-weight", "bold")
  .attr("dx", 12) // X 방향의 오프셋
  .attr("dy", ".35em"); // Y 방향의 오프셋

node.append("title").text((d) => d.id);

function ticked() {
  link
    .attr("x1", (d) => d.source.x)
    .attr("y1", (d) => d.source.y)
    .attr("x2", (d) => d.target.x)
    .attr("y2", (d) => d.target.y);
  node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
  labels
    .attr("x", (d) => d.x + 10) // X 위치 조정, 노드의 오른쪽에 위치
    .attr("y", (d) => d.y) // Y 위치를 노드 중심으로 설정
    .style("font-size", "12px")
    .style("fill", "#333")
    .style("font-weight", "bold")
    .attr("alignment-baseline", "middle") // 텍스트를 노드 중앙과 수평으로 맞춤
    .attr("text-anchor", "start"); // 텍스트가 시작점을 기준으로 렌더링되도록 설정
}

function drag(simulation) {
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }

  return d3
    .drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
}

simulation.on("tick", ticked);
display(svg.node());
```
