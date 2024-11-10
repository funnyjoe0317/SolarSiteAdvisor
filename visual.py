import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
# Shapefile 불러오기
gdf = gpd.read_file("buildings.shp")

# 건물 높이 정보가 포함된 DataFrame 생성
gdf["height"] = gdf["height"].fillna(10)  # NaN 값에 기본 높이 설정
df = pd.DataFrame(gdf)

# Plotly 3D scatter plot로 시각화
fig = px.scatter_3d(df, x="geometry.x", y="geometry.y", z="height",
                    color="height", height=600, title="건물 3D 시각화")
fig.show()
# # 기본 평면 시각화
# fig, ax = plt.subplots(1, 1, figsize=(10, 10))
# gdf.plot(ax=ax, color="lightblue", edgecolor="black")
# plt.title("건물 평면 정보 시각화")
# plt.xlabel("경도")
# plt.ylabel("위도")
# plt.show()
