import cv2
import numpy as np
import face_recognition
import os,pickle

class Signin:
    def __init__(self):
        pass

    def registerFace(self,id):
        count=0
        capture=cv2.VideoCapture(0)
        face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        if not os.path.exists(f'dataset/{id}'):
            os.mkdir(f'dataset/{id}')
        while True:
            _,img=capture.read()
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces=face_cascade.detectMultiScale(gray,1.1,4)
            for (x,y,w,h) in faces:
                count+=1
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)
                roi_gray=gray[y:y+h,x:x+w]
                roi_color=img[y:y+h,x:x+w]
                print('Capturing face dataset')
                cv2.imwrite(f'dataset/{id}/{id}_{count}'+'.jpg',roi_color)
        
            cv2.imshow('Register Face',img)
            if cv2.waitKey(1) & 0xff ==ord('q'):
                break
            elif count>=30:
                break
        capture.release()
        cv2.destroyAllWindows()
        self.writeEncodings(id)
        
    
    def writeEncodings(self,name):
        print('Started Encoding')
        dictEncoding={}
        path=f'dataset/{name}'
        files=os.listdir(path)
        dataset=[file for file in files if file.endswith(".jpg")]
        for img in dataset:
            curImg=cv2.imread(f'{path}/{img}')
            curImg=cv2.cvtColor(curImg,cv2.COLOR_BGR2RGB)
            try:
                encode=face_recognition.face_encodings(curImg)[0]
                dictEncoding[img]=encode
            except:
                dictEncoding[img]=np.zeros((128,))
        
        with open(f'{path}/encoding.pkl','wb') as f:
            pickle.dump(dictEncoding,f)
            
        print("Finished Encoding\n")
        
            
    
    def run(self):
        id=input("Enter mail id:").strip()
        name=id[:id.find("@gmail.com")]
        print(name)
        try:
            os.mkdir(f'dataset/{name}')
            self.registerFace(name)
            print('saved')
        except FileExistsError:
            overwrite=input("User already found. Overwrite ? [y/n]")
            if overwrite=='y':
                self.registerFace(name)
                print("Saved")


    
    

if __name__=='__main__':
    obj=Signin()
    obj.run()


