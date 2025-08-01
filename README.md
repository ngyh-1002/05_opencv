---

### 프로젝트 요약

#### 1. QR 코드 인식
- **목표:** 웹캠으로 QR 코드를 인식하고, 디코딩된 URL을 자동으로 웹 브라우저로 엽니다.
- **주요 기능:** 실시간 영상 처리, 코드 정보 시각화, 웹 브라우저 제어.

#### 2. 영상 캡처
- **목표:** 웹캠 영상의 현재 프레임을 사용자의 키 입력에 따라 이미지 파일로 저장합니다.
- **주요 기능:** 실시간 영상 캡처, 키 입력 감지, 파일 저장.

#### 3. 카메라 캘리브레이션
- **목표:** 체커보드 이미지를 분석하여 렌즈 왜곡을 보정하는 매개변수를 계산하고, 실시간 영상에 적용해 보정된 영상을 보여줍니다.
- **주요 기능:** 체커보드 코너 검출, 캘리브레이션 데이터 계산 및 저장, 실시간 왜곡 보정.

#### 4. ArUco 마커 거리 측정
- **목표:** 캘리브레이션 데이터를 활용해 ArUco 마커의 3D 위치(거리)와 방향을 실시간으로 추정하고 시각화합니다.
- **주요 기능:** 왜곡 보정, 마커 검출, 3D 포즈 추정, 결과 시각화.

---

### 프로젝트 순서도 및 상세 설명 (시각화 강화)

#### 1. QR 코드 인식 순서도

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
