import cv2
import numpy as np
import random

# 读取图像
image = cv2.imread("image.png")

# 检查图像是否成功加载
if image is None:
    print("Error: 无法加载图像。请检查文件路径。")
else:
    # 将彩色图像转换为灰度图像
    color_to_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 对灰度图像应用高斯模糊
    blur_image = cv2.GaussianBlur(color_to_gray, (3, 3), 0)

    # 使用Canny算法检测边缘
    edges = cv2.Canny(blur_image, threshold1=110, threshold2=110)

    # 查找轮廓
    contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 初始化列表
    contours_poly = [None] * len(contours)
    boundRect = [None] * len(contours)
    centers = [None] * len(contours)
    radius = [None] * len(contours)

    # 设置最小半径阈值和最小面积阈值
    min_radius = 60  # 您可以根据需要调整这个值
    min_area = 40  # 设置最小面积阈值

    # 遍历轮廓
    for i, c in enumerate(contours):
        # 轮廓近似
        contours_poly[i] = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
        # 计算边界矩形
        boundRect[i] = cv2.boundingRect(contours_poly[i])
        # 计算最小外接圆
        centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

        # 随机颜色
        color = (random.randint(50, 180), random.randint(50, 180), random.randint(50, 200))
        # 检查轮廓面积是否大于最小面积阈值
        area = cv2.contourArea(c)
        if area > min_area:
            # 绘制边界矩形
            cv2.rectangle(edges, (int(boundRect[i][0]), int(boundRect[i][1])), 
                          (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)
            
            # 只有当圆的半径大于最小半径阈值时才绘制
            if radius[i] > min_radius:
                # 绘制最小外接圆
                cv2.circle(edges, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)

    # 保存图像为JPG格式
    cv2.imwrite('processed_image.jpg', edges)

    # 显示仅包含轮廓和形状的图像
    cv2.imshow('Contours on Edges Background', edges)

    # 等待按键，0表示无限等待
    cv2.waitKey(0)

    # 关闭所有窗口
    cv2.destroyAllWindows()