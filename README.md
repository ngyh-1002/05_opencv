누락된 부분에 대해 죄송합니다. 사용자님의 코드에서 추가적으로 사용된 이미지 처리 기법들을 다시 분석하여, 그 기능과 사용된 이유를 상세히 포함하여 README 파일을 보강하겠습니다.

---

### 프로젝트 요약 (README)

#### 1. QR 코드 인식
- **목표:** 웹캠을 통해 QR 코드를 인식하고, 디코딩된 URL을 자동으로 웹 브라우저로 엽니다.
- **주요 기능:** 실시간 영상 처리, 코드 정보 시각화, 웹 브라우저 제어.

#### 2. 영상 캡처
- **목표:** 웹캠 영상의 현재 프레임을 사용자의 키 입력에 따라 이미지 파일로 저장합니다.
- **주요 기능:** 실시간 영상 캡처, 키 입력 감지, 파일 저장.

#### 3. 카메라 캘리브레이션
- **목표:** 체커보드 이미지를 분석하여 렌즈 왜곡을 보정하는 매개변수를 계산하고, 다양한 전처리 기법을 적용하여 코너 검출 성공률을 높입니다. 또한, 실시간 영상에 보정된 매개변수를 적용하여 왜곡된 영상을 보정합니다.
- **주요 기능:** 체커보드 코너 검출, 다양한 전처리(CLAHE, 가우시안 블러, 이진화), 캘리브레이션 데이터 계산 및 저장, 실시간 왜곡 보정.

#### 4. ArUco 마커 거리 측정
- **목표:** 캘리브레이션 데이터를 활용해 ArUco 마커의 3D 위치(거리)와 방향을 실시간으로 추정하고 시각화합니다.
- **주요 기능:** 왜곡 보정, 마커 검출, 3D 포즈 추정, 결과 시각화.

---

### 프로젝트 순서도 및 상세 설명

#### 1. QR 코드 인식 순서도

`cv2.VideoCapture(0)`
→ **카메라 객체(`cap`)** 생성

`cap.read()`
→ **프레임(`img`)** 획득
→ `ret`(성공 여부)

`cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`
→ `img`를 흑백으로 변환
→ **흑백 이미지(`gray`)**

`pyzbar.decode(gray)`
→ `gray`에서 QR 코드 디코딩
→ **디코딩 정보(`decoded`)**

`for d in decoded:`
  → `cv2.rectangle(img, ...)`
    → **`img`**에 사각형 그리기
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

`cv2.imread(fname)`
→ **이미지(`img`)** 획득
`cv2.cvtColor(img, ...)`
→ **흑백 이미지(`gray`)** 획득

**다양한 전처리 방법 테스트**
- `cv2.createCLAHE(...)`: **CLAHE 평탄화** 적용. 영상의 대비를 지역적으로 개선하여 어둡거나 밝은 영역의 디테일을 살립니다.
  - **결과:** `gray_clahe` (평탄화된 흑백 이미지)
- `cv2.GaussianBlur(gray, (5, 5), 0)`: **가우시안 블러** 적용. 이미지의 노이즈를 부드럽게 제거하여 코너 검출의 안정성을 높입니다.
  - **결과:** `gray_blur` (블러 처리된 흑백 이미지)
- `cv2.Laplacian(gray, cv2.CV_64F).var()`: **라플라시안 필터**를 사용해 이미지의 선명도(블러 정도)를 측정합니다. 이미지의 품질을 분석하는 데 사용됩니다.
  - **결과:** `laplacian_var` (선명도 값)
- `cv2.threshold(gray, ...)`: **이진화(Threshold)** 적용. 이미지를 흑과 백 두 가지 색으로만 구분하여 윤곽선을 명확하게 만듭니다.
  - **결과:** `gray_thresh` (이진화된 이미지)

**체커보드 코너 검출**
`cv2.findChessboardCorners(processed_gray, ...)`
→ `ret`(성공 여부)
→ **코너 좌표(`corners`)** 획득

`cv2.cornerSubPix(processed_gray, corners, ...)`
→ **정제된 코너 좌표(`corners2`)** 획득
→ `objpoints` 및 `imgpoints` 리스트에 데이터 추가

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

사용자님의 코드를 기반으로, 각 프로젝트의 메서드에 대한 상세한 설명과 순서도를 다시 정리해 드릴게요.

---

### 1. QR 코드 인식

- **`cv2.VideoCapture(0)`**: 컴퓨터에 연결된 카메라 장치에 접근하는 객체를 생성합니다. `0`은 일반적으로 내장 웹캠을 의미합니다. 이 객체를 **`cap`** 변수에 할당하여 카메라로부터 실시간 영상을 받아옵니다.
- **`cap.read()`**: **`cap`** 객체에서 현재 프레임 하나를 읽어옵니다. `ret` (boolean) 변수에 성공 여부를, `img` (numpy.ndarray) 변수에 이미지 데이터를 저장합니다.
- **`cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`**: 이미지의 색상 공간을 변환합니다. 웹캠이 읽어온 컬러 이미지 **`img`**를 **흑백(GRAYSCALE)** 이미지 **`gray`**로 변환합니다. 이는 QR 코드 인식 속도와 정확도를 높이기 위함입니다.
- **`pyzbar.decode(gray)`**: `pyzbar` 라이브러리의 핵심 함수로, 흑백 이미지 **`gray`**에서 QR 코드를 찾아 디코딩합니다. 인식된 코드들의 리스트를 **`decoded`**에 반환하며, 각 항목에는 코드의 데이터, 타입, 위치 정보 등이 포함됩니다.
- **`cv2.rectangle(img, pt1, pt2, color, thickness)`**: 이미지 **`img`**에 직사각형을 그립니다. **`d.rect`**의 좌표를 사용해 인식된 QR 코드 영역을 시각적으로 표시합니다.
- **`cv2.putText(img, text, org, font, fontScale, color, thickness, lineType)`**: 이미지 **`img`**에 텍스트를 그립니다. 디코딩된 데이터 `text`를 QR 코드 근처에 표시하여 사용자에게 정보를 보여줍니다.
- **`webbrowser.open(barcode_data)`**: `webbrowser` 라이브러리를 사용해 디코딩된 **`barcode_data`** (URL)를 기본 웹 브라우저로 엽니다.
- **`cv2.imshow('camera', img)`**: "camera"라는 제목의 창에 현재 프레임 **`img`**를 실시간으로 표시합니다.

---

### 2. 영상 캡처

- **`cv2.VideoCapture(0)`**: 카메라 객체 **`cap`**을 생성합니다.
- **`cap.read()`**: **`cap`**에서 프레임을 읽어와 **`frame`** 변수에 저장합니다.
- **`cv2.imshow("Video", frame)`**: "Video"라는 제목의 창에 현재 프레임 **`frame`**을 실시간으로 표시합니다.
- **`cv2.waitKey(1) & 0xFF`**: 1ms 동안 키보드 입력을 기다립니다. `& 0xFF`는 입력된 키의 아스키(ASCII) 코드 값을 정확히 추출하는 역할을 합니다.
- **`cv2.imwrite(filename, frame)`**: 현재 프레임 **`frame`**을 지정된 파일명 **`filename`**으로 저장합니다. 파일명은 `datetime` 라이브러리로 생성되어 중복되지 않도록 합니다.

---

### 3. 카메라 캘리브레이션

- **`cv2.imread(fname)`**: 체커보드 이미지 파일 **`fname`**을 읽어 **`img`** 변수에 저장합니다.
- **`cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`**: 이미지 **`img`**를 흑백 이미지 **`gray`**로 변환합니다.
- **`cv2.findChessboardCorners(image, patternSize, flags)`**: 흑백 이미지 **`gray`**에서 체커보드의 코너를 찾습니다. 성공 시 `ret`는 `True`가 되고, 코너들의 픽셀 좌표를 **`corners`**에 저장합니다.
- **`cv2.cornerSubPix(image, corners, winSize, zeroZone, criteria)`**: `findChessboardCorners`로 찾은 코너 좌표 **`corners`**를 더 정교하게 다듬습니다. 코너의 위치를 소수점 단위까지 정확하게 계산하여 **`corners2`**에 저장합니다.
- **`cv2.createCLAHE(clipLimit, tileGridSize)`**: **CLAHE(Contrast Limited Adaptive Histogram Equalization)** 평탄화 객체를 생성합니다. 이미지의 대비를 지역적으로 개선하여 어둡거나 밝은 영역의 디테일을 선명하게 만듭니다.
- **`cv2.GaussianBlur(src, ksize, sigmaX)`**: 이미지 **`src`**에 가우시안 블러 필터를 적용합니다. 노이즈를 부드럽게 제거하여 코너 검출의 안정성을 높입니다.
- **`cv2.threshold(src, thresh, maxval, type)`**: 이미지 **`src`**를 이진화(threshold)합니다. 픽셀 값이 `thresh`보다 크면 `maxval`로, 작으면 0으로 만듭니다. 체커보드처럼 흑백 대비가 뚜렷한 이미지에 유용합니다.
- **`cv2.Laplacian(src, ddepth)`**: 이미지 **`src`**에 라플라시안 필터를 적용하여 이미지의 선명도(sharpness)를 측정합니다. 반환된 값의 분산(variance)이 높을수록 이미지가 선명합니다.
- **`cv2.calibrateCamera(objectPoints, imagePoints, imageSize, ...)`**: 체커보드의 3D 월드 좌표(`objectPoints`)와 이미지 내 2D 코너 좌표(`imagePoints`)를 사용해 카메라의 내부 파라미터(**`mtx`**)와 렌즈 왜곡 계수(**`dist`**)를 계산합니다.
- **`cv2.undistort(src, cameraMatrix, distCoeffs, ...)`**: 왜곡된 이미지 **`src`**를 **`mtx`**와 **`dist`**를 사용하여 보정하고, 보정된 이미지 **`dst`**를 반환합니다.

---

### 4. ArUco 마커 거리 측정

- **`cv2.aruco.ArucoDetector(dictionary, parameters)`**: ArUco 마커 검출기 객체를 생성합니다. `dictionary`는 검출할 마커의 종류를 정의하고, `parameters`는 검출 방식을 설정합니다.
- **`detector.detectMarkers(image)`**: 검출기 객체 **`detector`**를 사용해 이미지 **`image`**에서 ArUco 마커를 찾습니다. 마커의 4개 코너 좌표들(**`corners`**)과 각 마커의 고유 ID(**`ids`**)를 반환합니다.
- **`cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)`**: PnP(Perspective-n-Point) 알고리즘을 사용해 마커의 3D 월드 좌표와 이미지 내 2D 좌표를 기반으로 카메라의 3D 포즈(위치와 방향)를 추정합니다.
    - **`rvec`**: 회전 벡터. 마커에 대한 카메라의 회전 정보를 담고 있습니다.
    - **`tvec`**: 이동 벡터. 마커로부터의 카메라 위치(x, y, z) 정보를 담고 있습니다.
- **`cv2.drawFrameAxes(image, cameraMatrix, distCoeffs, rvec, tvec, length)`**: 이미지 **`image`**에 3D 좌표축을 그립니다. **`rvec`**와 **`tvec`**를 사용해 마커의 3D 포즈를 시각적으로 표시합니다.
- **`cv2.aruco.drawDetectedMarkers(image, corners, ids)`**: 이미지 **`image`**에 검출된 마커 영역을 사각형으로 그립니다.
