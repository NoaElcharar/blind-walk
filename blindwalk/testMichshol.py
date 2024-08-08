
from block_new import*
from collections import Counter
import math
from PIL import Image, ImageDraw



#חישוב מרחק בין 2 נקודות
def distance_Oftwo_point(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


# פונקציה שמקבלת רשימת פיקסלים של גוש ומוצאת נקודות קצה בגוש
def find_extreme_points(blob_pixels):
    if not blob_pixels:
        return None, None, None, None
    arrSortX = sorted(blob_pixels, key=lambda point: (point[0], point[1]))
    arrSortY = sorted(blob_pixels, key=lambda point: (point[1], point[0]))   
    return arrSortX[0], arrSortX[-1],arrSortY[0], arrSortY[-1]




# פונקציה שמוצאת נקודת מרכז של גוש 
def center_point_of_a_block(pixels):
    
    # בדיקה אם רשימת הפיקסלים ריקה
    if not pixels:
        return None 
    total_x = sum(pixel[0] for pixel in pixels)
    total_y = sum(pixel[1] for pixel in pixels)
    centroid_x = total_x / len(pixels)
    centroid_y = total_y / len(pixels)
    return (centroid_x, centroid_y)


# פונקציה למציאת גודל גוש, מחזיר אורך ורוחב של הגוש
def rochavBlock(top,bottom,right,left):
    width = left - right
    length = top - bottom
    return width, length

# פיקסול תמונה
def pixelate_image(image, pixel_size):
    width, height = image.size
    # שינוי גודל תמונה
    small_img = image.resize(
        (width // pixel_size, height // pixel_size),
        resample=Image.NEAREST#פיקסל את הצבע הפיקסל הנוכחי לצבע השכן הסמוך לו  
    )
    # שמירת התמונה לפיקסול
    pixelated_img = small_img.resize(
        image.size,
        Image.NEAREST
    )
    return pixelated_img

# ומיקומי טווח הראיה| פונקציה שמסרטטת את הקו ראיה של המשתמש 
def sight_location(image, pixel_size):
    width, height = image.size
    half_height = height // 2
    # לצורך סרטוט על התמונה
    draw = ImageDraw.Draw(image)
    
    segment_width = width // 4
    # מיקום טווח הראיה 
    first_quarter_start = segment_width
    second_quarter_end = 3 * segment_width
    # סרטוט 
    draw.rectangle(
        (first_quarter_start, half_height, second_quarter_end, height), 
        outline='green', 
        width=pixel_size
    )
    return (first_quarter_start, half_height, second_quarter_end, height)


#-התיחסות מספר הצבעים num_colors| פונקציה שמחזירה גושי צבע מתמונה
def blockColor_to_matrix(img, step_size, similarity_threshold=120, num_colors=256):
   
    img_width = img.width - (img.width % step_size)
    img_height = img.height - (img.height % step_size)
    img_resized = img.resize((img_width, img_height), Image.LANCZOS)#שמירת איכות התמונה
    
    # לצורך חישוב נקודת מגוז בתמונה 
    ww,hh=img_resized.size
    point_magoz=(ww//2,hh//2)
    
    
    img_array = np.array(img_resized)
    
    #  וערכיו RGB משנה את המערך למטריצה 
    img_array = img_array.reshape((-1, 3))
    
    kmeans = KMeans(n_clusters=num_colors, random_state=0).fit(img_array)
    labels = kmeans.labels_               #מספר קבוצה שכל פיקסל שייך אליו 
    centers = kmeans.cluster_centers_     #צבע מרכזי בכל קבוצה 
    img_quantized = centers[labels].reshape((img_height, img_width, 3)).astype(np.uint8)     #כל פיקסל בצבע המרכזי של הקבוצה שייך מערך של פיקסלים עם 
    
    color_blocks = find_color_blocks(img_quantized)        #קריאה לפונקציה שמזהה גושים בתמונה 
    
    return color_blocks, img_quantized,point_magoz

#פונקציה מחשבת גובה של גוש י  
def height_block(pixeles):
    
    x_values = [point[0] for point in pixeles]
    x_counter = Counter(x_values)#כמה פעמים מופיה כל איקס
    
    most_common_x, _ = x_counter.most_common(1)[0]#האיקס הפופולארי ביותר חוזר 
    
    filtered_points = [point for point in pixeles if point[0] == most_common_x]#סינון הנקודות עם הערך איקס שחזר 
    min_point = min(filtered_points, key=lambda point: point[1])
    max_point = max(filtered_points, key=lambda point: point[1])
    return distance_Oftwo_point(min_point, max_point)


#   סידור וחישוב הגושים בתמונה פונקציה עיבוד תמונה שבה 
def process_frame(frame, pixel_size, display_size):
    
    # arr = [] # המערך שיתמלא כל פריים מחדש בזיהוי הגושים הנוכחיים 
    
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    pixelated_img = pixelate_image(img, pixel_size)
   
    green_area = sight_location(pixelated_img, pixel_size)
   
    # של התמונה לאחר Kmeans מערך הגושים ומטריצה 
    arrAllColor, green_matrix,point_magoz = blockColor_to_matrix(pixelated_img, 10)
   
   
    # סרטוט גושי טווח ראיה 
    # draw_contours(pixelated_img, arrAllColor, 10)
    
    # חישוב כף רגל
    len_foot = (green_area[3] - green_area[1]) // 25 

    for block in arrAllColor:
      
      loc_block = center_point_of_a_block(block['allPx'])   
     
      #בעבור כל פריים אני יחשב את המיקום שלי הנוכחי 
      my_loc = (green_area[3], len_foot)
      
     
      h = height_block(block['allPx'])
      
      #print(f"Centroid of the last row is at: {my_loc}") הדפסת מיקום שלי
      
      distance = distance_Oftwo_point(loc_block, my_loc)
      
      i = arrAllColor.index(block)
     
      arrAllColor[i] = {'allPx': block['allPx'], 
                        'distance': distance, 
                        'locBlock': loc_block, 
                        'height': h, 
                        'area': green_area, 
                        'myLoc':my_loc,
                        'color': block['color'],'point_magozh':point_magoz}
    #   print(f"The distance between {loc_block} and {my_loc} is {distance}")
      
    return arrAllColor



# גודל יחסי של גוש ביחס לתמונה כדי לבדוק אם משתנה בתמונה  -פונקציה להמרת גודל ורוחב של גוש מפיקסלים לאחוזים
def pixelToPercent(widthInPixles, heightInPixles, img):
    widthInPercent, heightInPercent = img.size
    widthInPercent = widthInPixles * 100 / widthInPercent
    heightInPercent = heightInPixles * 100 / heightInPercent
    return widthInPercent, heightInPercent


# פונקציה לבדוק אם וקטור התנועה של הגוש ושל העיוור מצביעים על התנגשות
def is_collision_possible(vector1, vector2):
    # חישוב הזווית בין שני הוקטורים
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]#חישוב מכפלה סקלרית 
    mag_v1 = math.sqrt(vector1[0]**2 + vector1[1]**2)#חישוב אורך של וקטור
    mag_v2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    cos_theta = dot_product / (mag_v1 * mag_v2)# בין שני הווקטורים חישוב הקוסינוס של הזווית 
    theta = math.acos(cos_theta)#חישוב הזווית 
    
    #  שאם הזווית בין הוקטורים קטנה מ-45 מעלות, יש סיכוי להתנגשות
    if theta < math.radians(45):
        return True
    return False

# חיסור בין שתי הנקודות | פונקציה לחישוב וקטור התנועה בין שתי נקודות
def calculate_vector(point1, point2):
    return (point2[0] - point1[0], point2[1] - point1[1])

# פונקציה לבדיקת מרחק וגובה של הגוש מהאדם
def testGo(block):
    # אם המרחק קטן ממאה 
    if distance_Oftwo_point(block['thitBlock']['myLoc'], block['thitBlock']['locBlock']) < 100:
    #    וגובה מכשול גדול מעשרים
        if height_block(block['thitBlock']['allPx']) > 20:
            # מחזיר מיקום מכשול 
            return "middle" if block['thitBlock']['area'][0] <= block['thitBlock']['locBlock'][0] <= block['thitBlock']['area'][2] else  "right" if block['thitBlock']['locBlock'][0] > block['thitBlock']['area'][2] else "left"
    return False


def main(video_path, pixel_size, display_size):
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return
    
    while True:
        # קריאת הפריים הראשון
        ret1, frame1 = cap.read()
        if not ret1:
            print("End of video ! or error reading the frame.")
            break
        
        # קריאת הפריים השני
        ret2, frame2 = cap.read()
        if not ret2:
            print("End of video! or error reading the frame.")
            break
        
        # עיבוד הפריימים
        allBlock1 = process_frame(frame1, pixel_size, display_size)
        allBlock2 = process_frame(frame2, pixel_size, display_size)
        
        arr_relative = []#מערך לבדיקת הגושים אם מהווים מכשול
        for curr_block in allBlock2:
            for prev_block in allBlock1:
                w_curr_block, h_curr_block = rochavBlock(*curr_block['area']) #חישוב אורך ורוחב גוש
                w_prev_block, h_prev_block = rochavBlock(*prev_block['area']) 
                # בדיקה אם מדובר באותו גוש 
                #     בדיקה אם ההפרש של המרחק של שתי הנקודות מרכז של הגוש שןןה להפרש של המרחק של כל גוש מהמיקום של המשתמש וכן בדיקה של הצבעים זההים
                if abs(curr_block['distance']-prev_block['distance']) == distance_Oftwo_point(curr_block['locBlock'], prev_block['locBlock']) and np.array_equal(curr_block['color'] ,prev_block['color']):
                    # יצירת מילון על הגוש הנוכחי 
                    temp = {'relative': pixelToPercent(w_prev_block, h_prev_block, frame2) / pixelToPercent(w_curr_block, h_curr_block, frame1),
                            'diffDistance': math.abs(curr_block['distance']-prev_block['distance']),
                            'distanceCenterBlock': distance_Oftwo_point(curr_block['locBlock'], prev_block['locBlock']),
                            'motionVectorBlock' : calculate_vector(prev_block['locBlock'], curr_block['locBlock']),
                            # 'motionVectorPerson' : calculate_vector(prev_block['locBlock'], curr_block['locBlock']),
                            # וקטור של קו ראיה 
                            'motionVectorPerson' : calculate_vector(curr_block['myLoc'], curr_block['point_magozh']),
                            'thitBlock': curr_block
                            }
                # גוש חדש שנכנס לפריים 
                else:
                    temp = {'relative': 0,
                            'diffDistance': curr_block['distance'],
                            'distanceCenterBlock': curr_block['locBlock'],
                            'motionVectorBlock' : 0,
                            'motionVectorPerson' : 0,
                            'thitBlock': curr_block
                            }
            arr_relative.append(temp) # כל הגושים המעודכנים 
        relative_values = [obj['relative'] for obj in arr_relative]
        counter = Counter(relative_values) #היחס הכי פופולרי להגדלה של גושים 

        # מוצאים את הערך עם מספר ההופעות הגבוה ביותר
        most_common_value = counter.most_common(1)[0][0]

# אם הגוש גדל יותר מהיחס הכללי או שזה גוש חדש צריך לבדוק אם מהווה מכשול

        arr_relative = [value for value in arr_relative if value['relative']>= most_common_value or value['relative'] == 0]
        for rel in arr_relative:
            #-גובה ומרחק אם זה גוש חדש או שהוקטורים נפגשים  בודק  אם הוא ממהווה מכשול  
            if rel['motionVectorBlock'] == 0 or rel['motionVectorPerson'] == 0 or is_collision_possible(rel['motionVectorBlock'], rel['motionVectorPerson']):
                message = testGo(rel)
            if message != False:
                print(message)
        
        # בדיקה אם יש ללחוץ על מקש 'q' כדי לצאת מהלולאה
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Video processing complete.")

# Example usage:
video_path = r"C:\project\UploadingPicture\wayperson.mp4"
pixel_size = 10
display_size = (640, 480)#גודל התמונה לאחר עיבוד 

main(video_path, pixel_size, display_size)



# #פונקציה שמסרטטת קוי מתאר מסביב לגוש
# def draw_contours(image, color_blocks, step_size):
#     # img = image.save(r"C:\project\UploadingPicture\wayperson.mp4")
#     img = cv2.imread(r"C:\project\UploadingPicture\wayperson.mp4")
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

























# # פונקציה שמקבלת את המטריצה לוקחת את השורה האחרונה ומחשבת את הנקודת מרכז שלה שזה המיקום של הלקוי ראיה
# def calculate_centroid_of_last_row(matrix):
   
#     # בדיקה שהמטריצה \השורה אחרונה לא ריקה 
#     if not matrix or not matrix[-1]:
#         return None  
    
#     last_row = matrix[-1]  # שורה אחרונה
#     total_x = sum(pixel[1][0] for pixel in last_row)  # Sum the x coordinates of pixels in the last row
#     centroid_x = total_x / len(last_row)  # Calculate the average x coordinate
#     centroid_y = last_row[0][1][1]  # y coordinate is the same for all pixels in the row
    
#     #מחזירה את הנקודת מרכז
#     return (centroid_x, centroid_y)





    # marked_img = Image.open(path_marked_img)
    # print("Green area matrix for the frame:")
    # # print_matrix(green_matrix)
    
    # marked_frame = cv2.cvtColor(np.array(marked_img), cv2.COLOR_RGB2BGR)
    
    # resized_frame = cv2.resize(marked_frame, display_size)
    
    # return resized_frame


# # פונקציה שמחזירה שיפוע 
# def M_Incline(x1,y1,x2,y2):
#     # if (x1==x2) or(y1==y2):
#     # קו אופקי
#     if  (x1==x2):
#         return 0
#     # כשאין משתנים שווים כדי שלא יהיה בעיה בחילוק עם אפס
#     m=(y1-y2)/(x1-x2)
#     return m





# # פונקציה שמדפיסהה את הצבעים של טווח ראיה 
# def print_matrix(matrix):
#     """
#     Print the matrix in a readable format.
#     """
#     for row in matrix:
#         print(" | ".join(str(pixel) for pixel in row))
    


# def find_extreme_points(blob_pixels):
#     if not blob_pixels:
#         return None, None, None, None
#     top_left = min(blob_pixels, key=lambda p: (p[0], p[1]))
#     bottom_right = max(blob_pixels, key=lambda p: (p[0], p[1]))
#     top_right = max(blob_pixels, key=lambda p: (p[0], -p[1]))
#     bottom_left = min(blob_pixels, key=lambda p: (p[0], -p[1]))
#     return top_left, bottom_right, top_right, bottom_left


# # נקודת חיתוך של שתי משוואות    
# def intersection_point(m1, c1, m2, c2):
#     # פתרון מערכת שתי המשוואות הישרות
#     if m1 == m2:
#         x=(c2 - c1)
#     else:
#         x = (c2 - c1) / (m1 - m2)
#     y = m1 * x + c1
#     print(x, y)
#     return x, y  
   
# # פונקציה שמחזירה שיפוע ך
# def M_Incline(x1,y1,x2,y2):
#     if (x1==x2):
#         return 0
#     #     or(y1==y2)
#     m=(y1-y2)/(x1-x2)
#     # c=y2-m*x2
#     return m





# #פונקציה שמחזירה חיתוך עם ציר Yי
# def c_of_axis(m,x2,y2):
#     c=y2-m*x2
#     return c  
  
# # פונקציה שבודקת אם הנקודה נמצאת בגבולות  של התמונה
# def is_point_in_image(x, y, width, height):
    
#     return 0 <= x < width and 0 <= y < height
      
