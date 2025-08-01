import cv2
import matplotlib.pyplot as plt
import pyzbar.pyzbar as pyzbar

img = cv2.imread('../img/frame.png')
# 스캔 이미지 그레이 스케일
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# plt.imshow(gray, cmap='gray')
# plt.show()

# 디코딩
decoded = pyzbar.decode(gray)
print(decoded)

for d in decoded:
    print(d.data.decode('utf-8'))
    print(d.type)

cv2.rectangle(img, (d.rect[0], d.rect[1]), (d.rect[0] + d.rect[2], d.rect[1] + d.rect[3]), (0, 255, 0), 2)

plt.imshow(img)
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()