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


