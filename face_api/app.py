#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:04:49 2019

@author: atta
"""


from api import insert_weights,identify,delete_weights,bulk_insert_weights
from flask import Flask, jsonify, request, redirect,make_response

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS_ZIP = {'zip'}


###############################################################################
###############################################################################
###############################################################################
###############################################################################




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
def allowed_file_zip(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_ZIP


@app.route('/identify', methods=['POST'])
def upload_image():
    
    try:
        # Check if a valid image file was uploaded
        if request.method == 'POST':
            if 'face' not in request.files:
                return redirect(request.url)

            file = request.files['face']
            user_id = request.values['user_id']

            if file.filename == '':
                return redirect(request.url)
        
        
            if request.values['user_id'] == '':
                result = {
                "error": True,
                "face_found_in_image": False,
                "face_match": False,
                "message": "No Unique User Id"
                }
                return make_response(jsonify(result),501)
        

            if file and allowed_file(file.filename):
                # The image file seems valid! Detect faces and return the result.
                return identify(user_id,file)

        # If no valid image file was uploaded, show the file upload form:
        result = {
                "error": True,
                "face_found_in_image": False,
                "face_match": False,
                "message": "Either File is Not image or No face in image"
                }
        return make_response(jsonify(result),501)


    except Exception as err :
        print(err)
        result = {
                "error": True,
                "face_found_in_image": False,
                "face_match": False,
                "message": err
                }
        
        return make_response(jsonify(result),501)
    
    
    
    
    
    
@app.route('/insert', methods=['POST'])
def insert_image():
    
    try:
        # Check if a valid image file was uploaded
        if request.method == 'POST':
            
            if 'face' not in request.files:
                return redirect(request.url)

            file = request.files['face']


            if file.filename == '':
                return redirect(request.url)
        
        
            if request.values['user_id'] == '':
                result = {
                "error": True,
                "face_found_in_image": False,
                "face_match": False,
                "message": "No Unique User Id"
                }
                return make_response(jsonify(result), status=501)
            else:
                user_id = request.values['user_id']
        

            
            if file and allowed_file(file.filename):
                # The image file seems valid! Detect faces and return the result.
                return insert_weights(user_id,file)
            
        # If no valid image file was uploaded, show the file upload form:
        result = {
                "error": True,
                "face_found_in_image": False,
                "face_match": False,
                "message": "Either File is Not image or No face in image"
                }
        return make_response(jsonify(result),501)
    
    
    except Exception as err:
        print(err)
        result = {
                "error": True,
                "face_found_in_image": False,
                "face_match": False,
                "message": err
                }
        return make_response(jsonify(result),501)








@app.route('/bulkInsert', methods=['POST'])
def bulk_insert_image():
    try:
        # Check if a valid image file was uploaded
        if request.method == 'POST':
            
            if 'face' not in request.files:
                return redirect(request.url)

            file = request.files['face']


            if file.filename == '':
                return redirect(request.url)
        
        
            if request.values['user_id'] == '':
                result = {
                "error": True,
                "face_found_in_image": False,
                "face_match": False,
                "message": "No Unique User Id"
                }
                return make_response(jsonify(result), status=501)
            else:
                user_id = request.values['user_id']
        

            
            if file and allowed_file_zip(file.filename):
                # The image file seems valid! Detect faces and return the result.
                return bulk_insert_weights(user_id,file)
            
        # If no valid image file was uploaded, show the file upload form:
        result = {
                "error": True,
                "face_found_in_image": False,
                "face_match": False,
                "message": "Either File is Not image or No face in image"
                }
        return make_response(jsonify(result),501)


    except Exception as err:
        print(err)
        result = {
                "error": True,
                "face_found_in_image": False,
                "face_match": False,
                "message": err
                }
        return make_response(jsonify(result),501)




@app.route('/delete', methods=['POST'])
def delete_image():
    
    try:
        # Check if a valid image file was uploaded
        if request.method == 'POST':
        
        
            if request.values['user_id'] == '':
                result = {
                "error": True,
                "message": "No Unique User Id"
                }
                return make_response(jsonify(result), status=501)
            else:
                user_id = request.values['user_id']
                return delete_weights(user_id)

            
                # If no valid image file was uploaded, show the file upload form:
            result = {
                    "error": True,
                    "message": "Unable To Delete Weights"
                    }
            return make_response(jsonify(result),501)

    except Exception as err :
        print(err)
        result = {
                "error": True,
                "message": err
                }
        return make_response(jsonify(result),501)






if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)