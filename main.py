import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote
# .env 파일의 환경 변수 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
api_key = os.getenv("KAKAO_API_KEY")

# API 요청에 필요한 주소
url = "https://dapi.kakao.com/v2/local/search/address.json"
headers = {
    "Authorization": f"KakaoAK {api_key}"
}

# 예시 주소
address = "경기도 성남시 분당구 서현동 84-6"
params = {"query": address}

# API 요청 보내기
response = requests.get(url, headers=headers, params=params)
result = response.json()

# 결과 출력
if result['documents']:
    latitude = result['documents'][0]['y']
    longitude = result['documents'][0]['x']
    print(f"주소: {address}")
    print("위도:", latitude)
    print("경도:", longitude)
else:
    print("해당 주소에 대한 정보를 찾을 수 없습니다.")


# 위도 경도에 따른 일사량 데이터 얻는 코드 
# API 기본 설정
base_url = "http://apis.data.go.kr/B551184/openapi/service/SolarGhiService/getSolarGhiHrInfo" # 실제 API Base URL로 변경

service_key = os.getenv("data_gongo")  # 공공데이터 포털에서 발급받은 디코딩된 인증 키 입력
# service_key = quote(os.getenv("data_gongo"))

# 요청 파라미터 설정
params = {
    "serviceKey": service_key,
    "pageNo": "1",
    "numOfRows": "10",
    "date": "20220105",          # YYYYMMDD 형식의 날짜
    "time": "1600",              # 시간을 요구하는 경우 추가 (예: 1600)
    "lat": latitude,
    "lon": longitude,
    "type": "json"           # 응답 타입 (JSON)
}

# 헤더 설정
headers = {
    "accept": "*/*"
}
# GET 요청 보내기
response = requests.get(base_url, params=params, headers=headers)

# 응답 상태 코드 및 내용 확인
print("응답 상태 코드:", response.status_code)
print("응답 내용:", response.text)

# 응답 상태 코드 및 내용 확인
print("응답 상태 코드:", response.status_code)
import xml.etree.ElementTree as ET
try:
    # JSON 응답 시도
    data = response.json()
    result_code = data['response']['header']['resultCode']
    result_msg = data['response']['header']['resultMsg']
    
    if result_code == "00":  # 성공 코드가 "00"인 경우
        items = data['response']['body']['items']['item']
        
        for item in items:
            date = item.get("Date")
            time = item.get("time")
            latitude = item.get("lat")
            longitude = item.get("lon")
            ghi = item.get("ghi")
            cghi = item.get("cghi")
            
            print(f"날짜: {date}, 시간: {time}, 위도: {latitude}, 경도: {longitude}, 일사량(GHI): {ghi}, 클라우드 적용 일사량(CGHI): {cghi}")
    else:
        print("API 요청 오류:", result_msg)

except requests.exceptions.JSONDecodeError:
    # XML 형식으로 응답이 올 때 처리
    root = ET.fromstring(response.content)
    result_code = root.find(".//resultCode").text
    result_msg = root.find(".//resultMsg").text
    print(f"오류 코드: {result_code}, 오류 메시지: {result_msg}")
    

import osmnx as ox
import geopandas as gpd

# 주소 또는 좌표 기반으로 OSM 데이터 가져오기
# address = "서울특별시 노원구 노원로 75"
# gdf = ox.geometries_from_place(address, tags={"building": True})

# 좌표 기반으로 특정 범위 지정하여 데이터 가져오기
latitude_float = float(latitude)
longitude_float=float(longitude)
center_point = (latitude_float, longitude_float)  # 위도, 경도 예시
print("Center Point (튜플):", center_point, type(center_point))  # 디버깅 출력
# gdf = ox.geometries_from_point(center_point, tags={"building": True}, dist=500)

try:
    # 반경을 넓혀서 시도 (1000미터)
    gdf = ox.features_from_point(center_point, tags={"building": True}, dist=1000)

    # 건물 높이 정보와 층수 필터링
    if not gdf.empty:
        gdf = gdf[["geometry", "height", "building:levels"]]
        print(gdf.head())

        # Shapefile로 저장
        gdf.to_file("buildings.shp", driver="ESRI Shapefile")
        print("파일이 성공적으로 저장되었습니다.")
    else:
        print("해당 위치 반경 내에 조건에 맞는 건물이 없습니다.")
        
except ox._errors.InsufficientResponseError:
    print("OSM 서버에서 조건에 맞는 데이터를 찾지 못했습니다. 태그나 반경을 조정해 보세요.")