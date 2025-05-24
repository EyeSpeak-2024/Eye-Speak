import numpy as np
import cv2
import mediapipe as mp
import time
import ctypes


class FaceControlledMouse:
    
    idx_list = [1, 33, 61, 199, 263, 291]
    RIGHT_EYE_IDX = [33, 159, 158, 133, 153, 145]
    LEFT_EYE_IDX = [362, 380, 374, 263, 386, 385]
    l_start = 0
    l_end = 0
    r_start = 0
    r_end = 0
    
    
    def __init__(self):
        self.solution = mp.solutions.face_mesh
        self.detector = self.solution.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.5,
        )
        self.drawer = mp.solutions.drawing_utils
        self.drawing_spec = self.drawer.DrawingSpec(color=(0,0,256),thickness=2,circle_radius=1)
        self.camera = cv2.VideoCapture(0)
        self.left_click = 0
        self.right_click = 0
        self.hold_left = False
        self.hold_right = False
        
    
        
    def mouse_move(self, event, dx, dy):
            # -x = right, -y = down 
            ctypes.windll.user32.mouse_event(event, dx, dy, 0, 0)
            
    # Blinking Ratio     
    
    def eye_aspect_ratio(self, eye_landmarks, landmarks):
        """
        Calculate the eye aspect ratio (EAR) for given eye landmarks.
        
        The EAR is calculated using the formula:
        EAR = (||p2-p6|| + ||p3-p5||) / (2||p1-p4||)
        where p1-p6 are specific points around the eye.
        
        Args:
            eye_landmarks (list): Indices of landmarks for one eye
            landmarks (list): List of all facial landmarks
        
        Returns:
            float: Calculated eye aspect ratio
        """
        A = np.linalg.norm(np.array(landmarks[eye_landmarks[1]]) - np.array(landmarks[eye_landmarks[5]]))
        B = np.linalg.norm(np.array(landmarks[eye_landmarks[2]]) - np.array(landmarks[eye_landmarks[4]]))
        C = np.linalg.norm(np.array(landmarks[eye_landmarks[0]]) - np.array(landmarks[eye_landmarks[3]]))
        return (A + B) / (2.0 * C)

    def wink_click(self, lwink_ratio, rwink_ratio):
        print(self.left_click)
        if not self.hold_left:

            if lwink_ratio < 0.23:
                
                
                if self.left_click == 0:
                    
                    self.left_click += 1
                    FaceControlledMouse.l_start = time.time()
                    self.mouse_move(0x0002, 0, 0)
                    self.mouse_move(0x0004, 0, 0)
                    
                elif self.left_click >= 1:
                    
                    FaceControlledMouse.l_end = time.time()
                    print("left hold: " + str(FaceControlledMouse.l_end - FaceControlledMouse.l_start))
                    if FaceControlledMouse.l_end - FaceControlledMouse.l_start > 0.1:
                        
                        print('HOLDING left')
                        FaceControlledMouse.l_start = 0
                        FaceControlledMouse.l_end = 0
                        self.left_click = 0
                        self.hold_left = True
                        print(self.hold_left)
                        self.mouse_move(0x0002, 0, 0)
                        
                    else:
                        self.mouse_move(0x0002, 0, 0)
                        self.mouse_move(0x0004, 0, 0)
                        FaceControlledMouse.l_start = 0
                        FaceControlledMouse.l_end = 0
                    
                        
                        
                else:
                    self.left_click += 1
                    
                    print("bro what")
                    
                    self.mouse_move(0x0002, 0, 0)
                    self.mouse_move(0x0004, 0, 0)
               
            else:
                print('NO CLICK')    
                
        elif self.hold_left:
            print('holding')
            if lwink_ratio > 0.26:
                self.left_click = 0
                self.mouse_move(0x0004, 0, 0)
                self.hold_left = False
                
                
        if not self.hold_right:

            if rwink_ratio < 0.23:
                
                
                if self.right_click == 0:
                    
                    self.right_click += 1
                    FaceControlledMouse.r_start = time.time()
                    self.mouse_move(0x0008, 0, 0)
                    self.mouse_move(0x0010, 0, 0)
                    
                elif self.right_click >= 1:
                    
                    FaceControlledMouse.r_end = time.time()
                    print("right hold: " + str(FaceControlledMouse.r_end - FaceControlledMouse.r_start))
                    if FaceControlledMouse.r_end - FaceControlledMouse.r_start > 0.1:
                        
                        print('HOLDING DOW right')
                        FaceControlledMouse.r_start = 0
                        FaceControlledMouse.l_end = 0
                        self.right_click = 0
                        self.hold_right = True
                        print(self.hold_right)
                        self.mouse_move(0x0008, 0, 0)
                        
                    else:
                        self.mouse_move(0x0008, 0, 0)
                        self.mouse_move(0x0010, 0, 0)
                        FaceControlledMouse.r_start = 0
                        FaceControlledMouse.r_end = 0
                    
                        
                        
                else:
                    self.right_click += 1
                    
                    print("bro what")
                    
                    self.mouse_move(0x0008, 0, 0)
                    self.mouse_move(0x0010, 0, 0)
                
        elif self.hold_right:
            print('holding')
            if rwink_ratio > 0.26:
                self.right_click = 0
                self.mouse_move(0x0010, 0, 0)
                self.hold_right = False

    
        
        
            
    def camera_on(self):
        cap = self.camera
        while cap.isOpened():
            success, image = cap.read()

            start = time.time()

            image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB) #flipped for selfie view
            image.flags.writeable = False
            results = self.detector.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
            
            img_h , img_w, img_c = image.shape
            face_2d = []
            face_3d = []

            landmarks_dict = {}
            
            if results.multi_face_landmarks:
                ######
                
                landmarks = results.multi_face_landmarks
                first_face_landmarks = landmarks[0]
                
                # Extract landmarks into a NumPy array
                np_landmarks = [
                    [landmark.x, landmark.y, landmark.z]
                    for landmark in first_face_landmarks.landmark
                ]

                landmarks_array = np.array(np_landmarks)
        
                #######
                
                for face_landmarks in landmarks:
                    for idx, lm in enumerate(face_landmarks.landmark):
                        if idx in FaceControlledMouse.idx_list:
                            if idx == 1:
                                nose_2d = (lm.x * img_w,lm.y * img_h)
                                nose_3d = (lm.x * img_w,lm.y * img_h,lm.z * 3000)
                            x,y = int(lm.x * img_w),int(lm.y * img_h)

                            face_2d.append([x,y])
                            face_3d.append(([x,y,lm.z]))

                    for ID, lm in enumerate(face_landmarks.landmark):
                        x, y = int(lm.x * img_w), int(lm.y * img_h)
                        landmarks_dict[ID] = (x, y)    

                
                    #Get 2d Coord
                    face_2d = np.array(face_2d,dtype=np.float64)

                    face_3d = np.array(face_3d,dtype=np.float64)

                    focal_length = 1 * img_w

                    cam_matrix = np.array([[focal_length,0,img_h/2],
                                        [0,focal_length,img_w/2],
                                        [0,0,1]])
                    distortion_matrix = np.zeros((4,1),dtype=np.float64)

                    success,rotation_vec,translation_vec = cv2.solvePnP(face_3d,face_2d,cam_matrix,distortion_matrix)


                    #getting rotational of face
                    rmat,jac = cv2.Rodrigues(rotation_vec)

                    angles,mtxR,mtxQ,Qx,Qy,Qz = cv2.RQDecomp3x3(rmat)
                    
                    
                    rwink_ratio = self.eye_aspect_ratio(FaceControlledMouse.RIGHT_EYE_IDX, landmarks_dict)
                    lwink_ratio = self.eye_aspect_ratio(FaceControlledMouse.LEFT_EYE_IDX, landmarks_dict)
                    ear = (rwink_ratio + lwink_ratio) / 2.0
                    print(ear)
                    if ear < 0.26:
                        print("blinking")
                    # print(blink_ratio)
                    

                    x = angles[0] * 360
                    y = angles[1] * 360
                    z = angles[2] * 360
                    
                    self.wink_click(lwink_ratio, rwink_ratio)

                    
                            
                    # print(self.hold_left)
                    # print("Left: " + str(lwink_ratio))
                    # print("Right: " + str(rwink_ratio))
                        
                        


                        

        
                        

                        
                    if y < -10:
                        text="Looking Left"
                        self.mouse_move(0x0001, -10, 0)
                    if y > 10:
                        text="Looking Right"
                        self.mouse_move(0x0001, 10, 0)
                    if x < -3:
                        text="Looking Down"
                        self.mouse_move(0x0001, 0, 10)
                    if x > 10:
                        text="Looking Up"
                        self.mouse_move(0x0001, 0, -10)
                    else:
                        text="Forward"

                    nose_3d_projection,jacobian = cv2.projectPoints(nose_3d,rotation_vec,translation_vec,cam_matrix,distortion_matrix)

                    p1 = (int(nose_2d[0]),int(nose_2d[1]))
                    p2 = (int(nose_2d[0] + y*10), int(nose_2d[1] -x *10))

                    cv2.line(image,p1,p2,(255,0,0),3)

                    cv2.putText(image,text,(20,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)
                    cv2.putText(image,"x: " + str(np.round(x,2)),(500,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    cv2.putText(image,"y: "+ str(np.round(y,2)),(500,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    cv2.putText(image,"z: "+ str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(image,str(lwink_ratio), (500, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(image,str(rwink_ratio), (500, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(image,str(ear), (500, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    


                end = time.time()
                totalTime = end-start

                try:
                    fps = 1/totalTime
                except:
                    fps = 0
                # print("FPS: ",fps)

                cv2.putText(image,f'FPS: {int(fps)}',(20,450),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,0),2)

                self.drawer.draw_landmarks(image=image,
                                        landmark_list=face_landmarks,
                                        connections=self.solution.FACEMESH_CONTOURS,
                                        landmark_drawing_spec=self.drawing_spec,
                                        connection_drawing_spec=self.drawing_spec)
            cv2.imshow('Head Pose Detection',image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        
# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5,min_tracking_confidence=0.5)

# mp_drawing = mp.solutions.drawing_utils

# drawing_spec = mp_drawing.DrawingSpec(color=(128,0,128),thickness=2,circle_radius=1)

f = FaceControlledMouse()
f.camera_on()
