import cv2
import numpy as np
import face_recognition
import os,pickle

class Login:
    def __init__(self):
        pass
    
    def readEncodings(self,name):
        path=f'dataset/{name}'
        with open(f'{path}/encoding.pkl','rb') as f:
            encodings=pickle.load(f)
        encodeList=list(encodings.values())
        return encodeList

    
    def Authenticate(self,encodeListKnown):
        cap=cv2.VideoCapture(0)
        while True:
            matched=0
            _,img = cap.read()
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            facesCurFrame=face_recognition.face_locations(img)
            encodesCurFrame=face_recognition.face_encodings(img,facesCurFrame)
            cv2.imshow('img',img)        
            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
                print(faceDis)
                matchIndex=np.argmin(faceDis)
                
                for i in faceDis:
                    if i<0.5:
                        matched+=1
                
            try:
                print(f'{matched}/{len(faceDis)}')
                if (matched/len(faceDis))>0.4:
                    print("Authentication Success")
                    return True
                    break
            except NameError:
                continue
            
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
    
    def run(self):
        id=input("Enter mail id:").strip()
        name=id[:id.find("@gmail.com")]
        print(name)
        try:
            encodeList=self.readEncodings(name)
            self.Authenticate(encodeList)
        except FileNotFoundError:
            print("Not registered")
if __name__=='__main__':
    obj=Login()
    obj.run()