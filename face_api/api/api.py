#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:58:08 2019

@author: atta
"""

from face_recognition import face_encodings,compare_faces,load_image_file
import sqlite3
import numpy as np
import io
from flask import jsonify, make_response
import zipfile



db_path = 'db/face_weights.sqlite'


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("array", convert_array)


def insert_weights(user_id,image):
    try:
        
        image = load_image_file(image)
        encoding = face_encodings(image)[0]
        
    except:
         result = {
                "error": True,
                "image_saved": False,
                "message": "Face Not Found"
                }
         return make_response(jsonify(result),501)
    
    try:
        
        if len(encoding) > 0:
            face_found = True
            
        else:
            result = {
                "error": True,
                "image_saved": False,
                "message": "Face Not Found"
                }
            return make_response(jsonify(result),501)
        
        
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        
        
        
        cur = conn.cursor()
        cur.execute('INSERT INTO face_encodings (user_id,encoding) values (?,?)', (user_id,encoding))
        
        conn.commit()
        conn.close()
        result = {
                "error": False,
                "image_saved": True,
                "message": "Success"
                }
        return make_response(jsonify(result),200)
    
    except Exception as err:
        print(err)
        msg = err
        status= 501
        conn.rollback()
        conn.close()
        
        result = {
                "error": True,
                "image_saved": False,
                "message": msg
                }
        return make_response(jsonify(result),status)
        
    
    
    

def identify(user_id,image):
    
    try:
        matched = False
        user_id = str(user_id)
        image = load_image_file(image)
        unknown_encoding = face_encodings(image)
        if len(unknown_encoding) > 0:
            face_found = True
        else:
            result = {
                "error": True,
                "image_saved": False,
                "message": "Face Not Found"
                }
        
            return make_response(jsonify(result),501)
        
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        
        cur = conn.cursor()
        
        cur.execute("select encoding from face_encodings where user_id =?",(user_id,))
        
        data = cur.fetchall()
        
        conn.close()
        
        data = np.array(data).tolist()
        
        
        for encodes in data:
           
            match_results = compare_faces([encodes[0]], unknown_encoding[0],tolerance=0.54)
            if match_results[0]:
                matched = True
                break;
        
                
        
        if matched:
            msg = "Success"
            status = 200
            result = {
                "error": False,
                "face_found_in_image": face_found,
                "face_match": matched,
                "message": msg
                }
            return make_response(jsonify(result),status)
        else:
            msg = "Face Not Matched"
            status = 501
            result = {
                "error": True,
                "face_found_in_image": face_found,
                "face_match": matched,
                "message": msg
                }
            return make_response(jsonify(result),status)
            
        
        
    except Exception as err:
         print(err)
         msg = err
         status= 501
         result = {
                "error": True,
                "face_found_in_image": face_found,
                "face_match": matched,
                "message": msg
                }
         return make_response(jsonify(result),status)
     
        
        
def delete_weights(user_id):
    
    try:
        
        
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        
        
        
        cur = conn.cursor()
        cur.execute('Delete from face_encodings where user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        result = {
                "error": False,
                "message": "Success {Weights Deleted}"
                }
        return make_response(jsonify(result),200)
    
    except Exception as err:
        print(err)
        msg = err
        status= 501
        conn.rollback()
        conn.close()
        
        result = {
                "error": True,
                "message": msg
                }
        return make_response(jsonify(result),status)



def bulk_insert_weights(user_id,image):
    try:
        conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        
        archive = zipfile.ZipFile(image, 'r')
        
        for finfo in archive.infolist():
            
            ifile = archive.open(finfo)
            #line_list = ifile.readlines()
            #archive.read(ifile.name)
            
            
            imgfile = load_image_file(ifile)
            
            
            encoding = face_encodings(imgfile)[0]
            
            if len(encoding) > 0:
                face_found = True
                
            else:
                result = {
                        "error": True,
                        "image_saved": False,
                        "message": "Face Not Found"
                }
                return make_response(jsonify(result),501)
            
            conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        
        
        
            cur = conn.cursor()
            cur.execute('INSERT INTO face_encodings (user_id,encoding) values (?,?)', (user_id,encoding))
            conn.commit()
        
        
        
        conn.close()
        result = {
                "error": False,
                "image_saved": True,
                "message": "Success"
                }
        return make_response(jsonify(result),200)
            
            
       
        
    except Exception as err:
         print(err)
         msg = err
         status= 501
         conn.rollback()
         conn.close()
         result = {
                "error": True,
                "image_saved": False,
                "message": msg
                }
         return make_response(jsonify(result),status)
    
        