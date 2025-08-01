

## 프로젝트 요약

### 1. QR 코드 인식
- **목표:** 웹캠으로 QR 코드를 인식하고, 디코딩된 URL을 자동으로 웹 브라우저로 엽니다.
- **주요 기능:** 실시간 영상 처리, 코드 정보 시각화, 웹 브라우저 제어.

### 2. 영상 캡처
- **목표:** 웹캠 영상의 현재 프레임을 사용자의 키 입력에 따라 이미지 파일로 저장합니다.
- **주요 기능:** 실시간 영상 캡처, 키 입력 감지, 파일 저장.

### 3. 카메라 캘리브레이션
- **목표:** 체커보드 이미지를 분석하여 렌즈 왜곡을 보정하는 매개변수를 계산하고, 실시간 영상에 적용해 보정된 영상을 보여줍니다.
- **주요 기능:** 체커보드 코너 검출, 캘리브레이션 데이터 계산 및 저장, 실시간 왜곡 보정.

### 4. ArUco 마커 거리 측정
- **목표:** 캘리브레이션 데이터를 활용해 ArUco 마커의 3D 위치(거리)와 방향을 실시간으로 추정하고 시각화합니다.
- **주요 기능:** 왜곡 보정, 마커 검출, 3D 포즈 추정, 결과 시각화.



## 프로젝트 순서도 및 상세 설명 (시각화 강화)

### 1. QR 코드 인식 순서도

`cv2.VideoCapture(0)`
→ **카메라 객체(`cap`)** 생성

`cap.read()`
→ **프레임(`img`)** 획득
→ `ret`(성공 여부)

`cv2.cvtColor(img, ...)`
→ `img`를 흑백으로 변환
→ **흑백 이미지(`gray`)**

`pyzbar.decode(gray)`
→ `gray`에서 QR 코드 디코딩
→ **디코딩 정보(`decoded`)**

`for d in decoded:`
  → **`d.rect`** (QR 코드 위치)
  → `cv2.rectangle(img, ...)`
    → **`img`**에 사각형 그리기
  → **`d.data.decode()`** (QR 코드 데이터)
  → `cv2.putText(img, ...)`
    → **`img`**에 텍스트 표시
  → `webbrowser.open(barcode_data)`
    → **웹 브라우저 열기**

`cv2.imshow('camera', img)`
→ **`img`**를 화면에 표시

---

#### 2. 영상 캡처 순서도

`cv2.VideoCapture(0)`
→ **카메라 객체(`cap`)** 생성

`cap.read()`
→ **프레임(`frame`)** 획득

`cv2.imshow("Video", frame)`
→ **`frame`**을 화면에 표시

`cv2.waitKey(1)`
→ `'a'` 키 입력 대기

`cv2.imwrite(filename, frame)`
→ **`frame`**을 **파일**로 저장

---

#### 3. 카메라 캘리브레이션 순서도

**반복문 (모든 체커보드 이미지에 대해)**
  `cv2.imread(fname)`
  → **이미지(`img`)** 획득
  `cv2.cvtColor(img, ...)`
  → **흑백 이미지(`gray`)** 획득
  `cv2.findChessboardCorners(gray, ...)`
  → `ret`(성공 여부)
  → **코너 좌표(`corners`)** 획득
  `cv2.cornerSubPix(gray, corners, ...)`
  → **정제된 코너 좌표(`corners2`)** 획득
  → `objpoints` 및 `imgpoints` 리스트에 데이터 추가
**루프 종료**

`cv2.calibrateCamera(objpoints, imgpoints, ...)`
→ **카메라 행렬(`mtx`)**
→ **왜곡 계수(`dist`)**

`cv2.undistort(frame, mtx, dist, ...)`
→ **왜곡 보정된 프레임(`dst`)** 획득

`cv2.imshow(...)`
→ 원본과 보정된 영상을 화면에 표시

---

#### 4. ArUco 마커 거리 측정 순서도

**캘리브레이션 데이터 로드**
→ **`mtx`, `dist`** 획득

`cv2.undistort(frame, mtx, dist, ...)`
→ **왜곡 보정된 프레임(`frame_undistorted`)**

`detector.detectMarkers(frame_undistorted)`
→ **마커 코너(`corners`)**
→ **마커 ID(`ids`)**

`if ids is not None:`
  → **마커별 루프**
  `cv2.solvePnP(corners[i], ...)`
    → **회전 벡터(`rvec`)**
    → **이동 벡터(`tvec`)**
  `cv2.drawFrameAxes(frame_undistorted, ...)`
    → **`frame_undistorted`**에 좌표축 그리기
  `cv2.putText(frame_undistorted, ...)`
    → **`frame_undistorted`**에 텍스트 표시

`cv2.imshow(...)`
→ 시각화된 **`frame_undistorted`**를 화면에 표시

네, 알겠습니다. 각 프로젝트별로 사용된 OpenCV 메서드들의 기능을 더 상세하게, 그리고 직관적으로 이해할 수 있도록 다시 정리해 드리겠습니다.

---

### 프로젝트 1: QR 코드 인식

- **`cv2.VideoCapture(0)`**: 컴퓨터에 연결된 카메라 장치에 접근하는 객체를 생성합니다. 인자로 `0`을 주면 일반적으로 시스템의 첫 번째 카메라(내장 웹캠)를 사용합니다. 이 객체를 통해 카메라로부터 실시간 영상 프레임을 받아올 수 있습니다.
- **`cap.read()`**: 카메라 객체 `cap`에서 현재 프레임 하나를 읽어옵니다.
    - **`ret`** (boolean): 프레임을 성공적으로 읽었는지 여부를 반환합니다. 성공하면 `True`, 실패하면 `False`입니다.
    - **`img`** (numpy.ndarray): 읽어온 컬러 이미지 프레임 데이터입니다.
- **`cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`**: 이미지의 색상 공간을 변환하는 함수입니다. 웹캠이 읽어온 **BGR** (파란색, 초록색, 빨간색) 형식의 컬러 이미지를 **흑백(GRAY)** 이미지로 바꿔줍니다. 흑백으로 변환하면 QR 코드 인식 속도와 정확도가 향상될 수 있습니다.
- **`pyzbar.decode(gray)`**: `pyzbar` 라이브러리의 핵심 함수로, 입력된 흑백 이미지 `gray`에서 QR 코드나 바코드를 찾아 디코딩합니다. 인식된 코드들의 리스트를 반환하며, 각 리스트 항목에는 코드의 데이터, 타입, 그리고 이미지 내의 위치 정보(`rect`)가 포함됩니다.
- **`cv2.rectangle(img, pt1, pt2, color, thickness)`**: 이미지 `img`에 직사각형을 그리는 함수입니다. QR 코드가 인식된 영역을 **`(d.rect[0], d.rect[1])`** 에서 **`(d.rect[0]+d.rect[2], d.rect[1]+d.rect[3])`** 까지 초록색으로 그려 사용자가 코드의 위치를 시각적으로 확인할 수 있게 합니다.
- **`cv2.putText(img, text, org, font, fontScale, color, thickness, lineType)`**: 이미지 `img`에 텍스트를 그리는 함수입니다. 디코딩된 데이터 `text`를 QR 코드 위쪽 위치에 노란색으로 표시합니다.
- **`cv2.imshow(winname, mat)`**: 윈도우 창을 생성하고, 그 창에 이미지 `mat`를 표시합니다. `winname`은 창의 제목이 됩니다.

---

### 프로젝트 2: 영상 캡처

- **`cv2.VideoCapture(0)`**: 프로젝트 1과 동일하게 카메라 객체를 생성합니다.
- **`cap.read()`**: 카메라로부터 프레임을 읽어와 `frame` 변수에 저장합니다.
- **`cv2.imshow("Video", frame)`**: "Video"라는 제목의 창에 현재 프레임 `frame`을 실시간으로 표시합니다.
- **`cv2.waitKey(1)`**: 지정된 시간(1ms) 동안 키보드 입력을 기다립니다. 아무 키도 눌리지 않으면 `-1`을 반환합니다. 사용자가 `'q'` 또는 `'a'` 키를 누르면 해당 키의 아스키(ASCII) 코드를 반환하여 프로그램 흐름을 제어합니다.
- **`cv2.imwrite(filename, img)`**: 지정된 파일명 `filename`으로 이미지 `img`를 파일로 저장합니다. 여기서는 `datetime` 라이브러리를 활용해 현재 날짜와 시간이 포함된 고유한 파일명을 생성하여 캡처 이미지를 저장합니다.

---

### 프로젝트 3: 카메라 캘리브레이션

- **`cv2.imread(fname)`**: 지정된 경로 `fname`의 이미지 파일을 읽어 `img` 변수에 저장합니다.
- **`cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`**: 캘리브레이션은 흑백 이미지에서 더 효율적이므로, 컬러 이미지 `img`를 흑백 이미지 `gray`로 변환합니다.
- **`cv2.findChessboardCorners(image, patternSize, flags)`**: 흑백 이미지 `image`에서 `patternSize`에 맞는 체커보드 코너들을 찾습니다. 성공적으로 코너를 찾으면 `True`를 반환하고, 코너 좌표들을 `corners`에 저장합니다.
- **`cv2.cornerSubPix(image, corners, winSize, zeroZone, criteria)`**: `findChessboardCorners`로 찾은 코너의 좌표를 더 높은 정확도로 정제합니다. 픽셀 단위보다 더 정교한 소수점 단위의 코너 위치를 얻을 수 있습니다.
- **`cv2.calibrateCamera(objectPoints, imagePoints, imageSize, ...)`**: 캘리브레이션의 핵심 함수입니다. 체커보드 3D 월드 좌표(`objectPoints`)와 이미지 내 2D 코너 좌표(`imagePoints`)를 사용해 카메라의 내부 파라미터(`camera_matrix`)와 렌즈 왜곡 계수(`dist_coeffs`)를 계산합니다.
- **`cv2.undistort(src, cameraMatrix, distCoeffs, ...)`**: 왜곡된 이미지 `src`를 카메라 행렬 `cameraMatrix`와 왜곡 계수 `distCoeffs`를 사용하여 왜곡을 보정하고, 보정된 이미지 `dst`를 반환합니다.

---

### 프로젝트 4: ArUco 마커 거리 측정

- **`cv2.aruco.ArucoDetector(...)`**: ArUco 마커 검출을 위한 객체를 생성합니다. 사전에 정의된 마커 딕셔너리(`DICT_5X5_100`)와 파라미터를 설정합니다.
- **`detector.detectMarkers(image)`**: 검출기 객체 `detector`를 사용해 이미지 `image`에서 ArUco 마커를 찾습니다. 마커의 4개 코너 좌표들(`corners`)과 각 마커의 고유 ID(`ids`)를 반환합니다.
- **`cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)`**: PnP (Perspective-n-Point) 알고리즘을 사용하여 3D 월드 좌표(`objectPoints`)와 2D 이미지 좌표(`imagePoints`)의 대응 관계를 기반으로 카메라의 3D 포즈(위치와 방향)를 추정합니다.
    - **`rvec`**: 회전 벡터. 카메라가 마커를 바라볼 때의 회전 정보를 담고 있습니다.
    - **`tvec`**: 이동 벡터. 카메라가 마커로부터 얼마나 떨어져 있는지(x, y, z)에 대한 정보를 담고 있습니다.
- **`cv2.drawFrameAxes(image, cameraMatrix, distCoeffs, rvec, tvec, length)`**: 이미지 `image`에 3D 좌표축(X: 빨강, Y: 초록, Z: 파랑)을 그립니다. `rvec`와 `tvec`를 사용하여 마커의 3D 포즈를 시각화합니다.
