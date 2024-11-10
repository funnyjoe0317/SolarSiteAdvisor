import xarray as xr
import matplotlib.pyplot as plt
import os
# NetCDF 파일 경로 설정
nc_file_path = "C:/pot/sun/sun_mon/KMAPP_solar_FWS_01M_mean.nc"

# 파일이 있는지 확인
if not os.path.exists(nc_file_path):
    print(f"파일 경로를 다시 확인하세요. 파일이 존재하지 않습니다: {nc_file_path}")
    exit()

try:
    # NetCDF 파일 불러오기
    data = xr.open_dataset(nc_file_path, engine='netcdf4')
    print("파일을 성공적으로 불러왔습니다.")
except FileNotFoundError:
    print("check file -D.")
    exit()  # 파일을 찾지 못하면 이후 코드 실행을 막음
except OSError as e:
    print(f"파일을 열 수 없습니다. OSError: {e}")
    exit()  # 파일을 열지 못하면 이후 코드 실행을 막음
except Exception as e:
    print(f"알 수 없는 오류 발생: {e}")
    exit()  # 다른 예외 발생 시 종료

# 파일이 제대로 열렸을 때만 이후 코드 실행
try:
    # 데이터셋 확인
    print(data)

    # 각 변수에 대한 상세 메타데이터 확인
    for var in data.data_vars:
        print("===================================")
        print(f"\nVariable: {var}")
        print(data[var])

    # # 변수 'SWDN_topo' 접근 (일사량 데이터)
    # swdn_topo = data['SWDN_topo']

    # # 데이터의 형태 및 정보 확인
    # print(swdn_topo)

    # # 특정 위치에서 시간대별 일사량 변화를 시각화합니다.
    # # 예를 들어 첫 번째 격자 (X=0, Y=0)의 일사량을 확인합니다.
    # # NetCDF 파일에는 시간 축이 없으므로 여기서는 공간의 특정 지점에서 데이터를 확인하는 형태입니다.
    # # specific_point_data = swdn_topo.isel(X=0, Y=0)
    # specific_point_value = swdn_topo.isel(X=100, Y=100).values
    # print(f"특정 지점 (X=100, Y=100)의 일사량 값: {specific_point_value} W/m^2")    

    # # 특정 Y 라인의 모든 X 좌표를 따라가는 데이터 시각화
    # specific_y_line = swdn_topo.isel(Y=100)
    
    # # 특정 지점에서의 일사량 데이터 시각화
    # plt.figure(figsize=(10, 6))
    # # specific_point_data.plot()
    # specific_y_line.plot()
    # # plt.title("Insolation at Specific Location (X=0, Y=0)")
    # plt.title("Insolation across X coordinates at Y=100")
    # plt.xlabel("X Coordinate")
    # plt.ylabel("Insolation (W/m^2)")
    # plt.grid()
    # plt.show()

except KeyError as e:
    print(f"데이터셋에서 변수 오류: {e}")
except Exception as e:
    print(f"알 수 없는 오류 발생: {e}")
