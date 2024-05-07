---
title: 관악02 노선도
theme: dashboard
toc: false
---

<style>
  @import url("https://fonts.googleapis.com/css?family=Noto+Serif+KR&display=swap");
  body {
    font-family: "Noto Serif KR", serif;
  }
</style>

# 관악02 노선도

관악02 노선도를 구글 지도 API Marker 기능을 활용해 보여줍니다.

<html>
<head>
    <title>관악02 노선도</title>
    <style>
        /* Set the size of the map */
        #map {
            height: 600px;
            width: 100%;
        }
         .price-tag {
            background-color: #4285F4;
            border-radius: 8px;
            color: #FFFFFF;
            font-size: 14px;
            padding: 10px 15px;
            position: relative;
        }
        .price-tag::after {
            content: "";
            position: absolute;
            left: 50%;
            top: 100%;
            transform: translate(-50%, 0);
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-top: 8px solid #4285F4;
        }
    </style>
    <script>
        let map;
        let markers = [];
        function initMap() {
            const mapCenter = { lat: 37.466977, lng: 126.957774 };
            // Initialize the map
            map = new google.maps.Map(document.getElementById("map"), {
                zoom: 14,
                center: mapCenter,
            });
            // Array of bus stops data
            const busStops = [
                { lat: 37.466977, lng: 126.957774, title: "가족생활동" },
                { lat: 37.466361, lng: 126.957690, title: "가족생활동" },
                { lat: 37.447169, lng: 126.949799, title: "건설환경종합연구소" },
                { lat: 37.455119, lng: 126.954467, title: "공동기기원" },
                { lat: 37.456071, lng: 126.955349, title: "교수회관입구" },
                { lat: 37.46046371, lng: 126.956766, title: "기숙사삼거리" },
                { lat: 37.47707918, lng: 126.9619752, title: "낙성대역" },
                { lat: 37.4775169, lng: 126.9594607, title: "낙성대입구" },
                { lat: 37.47487295, lng: 126.9591501, title: "낙성대현대아파트" },
                { lat: 37.4587949, lng: 126.955328, title: "노천강당" },
                { lat: 37.46233612, lng: 126.9573923, title: "대학원생활관" },
                { lat: 37.46872249, lng: 126.9579992, title: "서울융합과학관" },
                { lat: 37.46802075, lng: 126.9612872, title: "인헌아파트" },
                { lat: 37.47710724, lng: 126.9617606, title: "인헌초등학교" },
                { lat: 37.44808487, lng: 126.9521426, title: "제2공학관" },
                { lat: 37.46314183, lng: 126.9577174, title: "학부생활관" },
                { lat: 37.46825784, lng: 126.9578128, title: "호암교수회관" },
                { lat: 37.46845638, lng: 126.9583385, title: "호암교수회관" },
                { lat: 37.45349631, lng: 126.9502262, title: "신소재" },
                { lat: 37.45359525, lng: 126.9522142, title: "에너지자원연구원" },
                { lat: 37.4487952, lng: 126.9520773, title: "제2공학관" },
                { lat: 37.44919617, lng: 126.9495359, title: "제2파워플랜트" },
            ];
            // Loop through the bus stops and place a marker for each
            busStops.forEach(function(stop) {
                let marker = new google.maps.Marker({
                    position: { lat: stop.lat, lng: stop.lng },
                    map: map,
                    title: stop.title
                });
                markers.push(marker);
            });
        }
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=&callback=initMap" async defer></script>

</head>
<body>
    <div id="map"></div>
</body>
</html>
