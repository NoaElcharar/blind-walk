import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
from collections import deque
import math




# רשימה של טפלים שכל זוג מספרים מייצג וקטור בכיוון מסוים.

directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]



# פונקציה שמשווה שתי צבעים ובודקת אם הם דומים
def is_similar_color(color1, color2, threshold=80):
    #   כלומר את אורך הוקטור ואם המרחק קטן מהסף זה אומר שהצבעים דומים ממיר את הצבעים למערך מחסר בינהם ומחשב את הנורמה של ההפרש
   
    return np.linalg.norm(np.array(color1) - np.array(color2)) < threshold





# ובודקת אם הוא לא חרג מגבולות התמונה וללא נבדק והצבע שלו דומה לצבע הנבדק פונקציה שבודקת מיקום של פיקסל שנשלח 
def is_valid_move(matrix, visited, color, x, y):
    rows, cols, _ = matrix.shape     
    return 0 <= x < rows and 0 <= y < cols and not visited[x][y] and is_similar_color(matrix[x, y], color)



# פונקציה שמחזירה רשימה של פיקסלים השייכת  לגוש של צבע 
def dfs(matrix, visited, color, x, y):
    stack = [(x, y)]
    
    #מכניסה למטריצה במיקום של הפיקסל ערך אמת שנבדק 
    visited[x][y] = True
   
    #רשימת הפיקסלים של הגוש 
    color_block = {'color': color, 'allPx': [(x, y)]}
   
    while stack:
        current_x, current_y = stack.pop()                            
        for dx, dy in directions:                                     
            new_x, new_y = current_x + dx, current_y + dy   
            if is_valid_move(matrix, visited, color, new_x, new_y):  
                stack.append((new_x, new_y))     
                
                visited[new_x][new_y] = True  
                color_block['allPx'].append((new_x, new_y))                   
    return color_block




# פונקציה שעוברת על כל המטריצה ומוצאת גושים בעזרת שימוש בפו חיפוש גןש dfs
def find_color_blocks(matrix):
   
   
    rows, cols, _ = matrix.shape
    
    #מטריצה בוליאנית שבה יוכנס הערך אם פיקסל נבדק או לא גודל כגודל התמונה 
    #בהתחלה כולם לא נבדקו-false 
    
    visited = np.zeros((rows, cols), dtype=bool)
    
    color_blocks = []
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                
                color_block = dfs(matrix, visited, matrix[i, j], i, j)
                color_blocks.append(color_block)
                
    return color_blocks








# # פונקציה שמקבלת תמונה ומזהה גושים בתמונה 
# def downsample_pixels(image_path, step_size, similarity_threshold=120, num_colors=256):
#     """
#     פונקציה זו מבצעת צמצום של רמת הפיקסלים בתמונה ושומרת את ערכי ה-RGB והמיקומים במטריצה.
#     """
#     # השינוי של הפיקסול
#     img = Image.open(image_path)
#     img_width = img.width - (img.width % step_size)
#     img_height = img.height - (img.height % step_size)
#     img_resized = img.resize((img_width, img_height), Image.LANCZOS)
#     img_array = np.array(img_resized)
#     # משנה את המערך למטריצה 
#     img_array = img_array.reshape((-1, 3))
    
#     # שימוש באלגוריתם k-means לצמצום צבעים
#     kmeans = KMeans(n_clusters=num_colors, random_state=0).fit(img_array)
#     labels = kmeans.labels_
#     centers = kmeans.cluster_centers_

#     img_quantized = centers[labels].reshape((img_height, img_width, 3)).astype(np.uint8)
#     color_blocks = find_color_blocks(img_quantized)#קריאה לפונקציה שמזהה גושים בתמונה 
    
#     return color_blocks

# #פונקציה שמסרטטת קוי מתאר מסביב לגוש
# def draw_contours(image, color_blocks, step_size):
#     img = image.save(r"C:\Users\User\Downloads\pixelated_image.jpg")
#     img = cv2.imread(r"C:\Users\User\Downloads\pixelated_image.jpg")
#     new_width = img.shape[1] // step_size * step_size
#     new_height = img.shape[0] // step_size * step_size
#     img_resized = cv2.resize(img, (new_width, new_height))

#     for color_block in color_blocks:
#         mask = np.zeros((new_height, new_width), dtype=np.uint8)

#         for point in color_block['allPx']:
#             mask[point[0], point[1]] = 255

#         # שיפור המסכה על ידי דילול והתרחבות
#         kernel = np.ones((3, 3), np.uint8)
#         mask = cv2.dilate(mask, kernel, iterations=1)
#         mask = cv2.erode(mask, kernel, iterations=1)

#         # מציאת קווי המתאר
#         contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         # ציור קווי המתאר על התמונה
#         cv2.drawContours(img_resized, contours, -1, (0, 255, 0), 1)

    # return img_resized

# # נתיב לתמונה במחשב שלך
# image_path = r"C:\project\UploadingPicture\ddd7.png"


# step_size = 10
# similarity_threshold = 60  # עדכון הסף להתאמת צבעים
# num_colors = 10  # מספר הצבעים לצמצום באלגוריתם k-means

# # מצמצם את רמת הפיקסלים ומחזיר את המערכים של גושי הצבעים
# color_blocks = color_to_matrix(image_path, step_size, similarity_threshold, num_colors)

# # מצייר את קווי המתאר סביב כל גוש ושומר את התמונה המעודכנת
# contoured_image = draw_contours(image_path, color_blocks, step_size)
# cv2.imwrite(r"C:\project\UploadingPicture\uyyy111.png", contoured_image)

# print("התמונה עם קווי המתאר נשמרה בהצלחה")
