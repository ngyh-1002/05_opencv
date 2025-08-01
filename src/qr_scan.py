import cv2
import matplotlib.pyplot as plt
import pyzbar.pyzbar as pyzbar
import webbrowser
import time

img1 = cv2.imread('../img/frame.png')
# plt.imshow(gray, cmap='gray')
# plt.show()

cap = cv2.VideoCapture(0)

while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        continue
    # 스캔 이미지 그레이 스케일
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 디코딩
    decoded = pyzbar.decode(gray)
    #print(decoded)

    for d in decoded:
        # print(d.data.decode('utf-8'))
        barcode_data = d.data.decode('utf-8')
        # print(d.type)
        barcode_type = d.type

        text = '%s (%s)' % (barcode_data, barcode_type)

        cv2.rectangle(img, (d.rect[0], d.rect[1]), (d.rect[0] + d.rect[2], d.rect[1] + d.rect[3]), (0, 255, 0), 20)
        cv2.putText(img, text, (d.rect[0], d.rect[1]-50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 3, (0, 255, 255), 2, cv2.LINE_AA)
        if decoded:
            print(f"Opening {barcode_data} in your default web browser...")
            webbrowser.open(barcode_data) # 기본 브라우저로 새 탭/창 열기

            # 새 창으로 열려면:
            # webbrowser.open(barcode_data, new=1)

            # 새 탭으로 열려면:
            # webbrowser.open(barcode_data, new=2)

            # 잠시 기다려 브라우저가 열리는 것을 확인
            time.sleep(2)
            print("Browser opened successfully (hopefully!).")
    cv2.imshow('camera', img)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
# plt.imshow(img)
# plt.show()
