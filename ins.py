from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
import uuid
import os

# Initialize Flask app
app = Flask(__name__)

# Firebase Configuration
cred = credentials.Certificate("C:\\Users\\vivek\\OneDrive\\Desktop\\Code\\python\\invisible\\credentials.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-storage-bucket.appspot.com'
})
db = firestore.client()
bucket = storage.bucket()

@app.route('/signin', methods=['POST'])
def sign_in():
    email = request.json['email']
    password = request.json['password']
    try:
        user = auth.get_user_by_email(email)
        return jsonify({'message': 'User signed in', 'user_id': user.uid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/create_post', methods=['POST'])
def create_post():
    data = request.json
    post_data = {
        "text": data['text'],
        "user": data['user'],
        "likes": 0,
        "comments": []
    }
    db.collection('posts').add(post_data)
    return jsonify({'message': 'Post created'}), 201

@app.route('/get_posts', methods=['GET'])
def get_posts():
    posts_ref = db.collection('posts').stream()
    posts = [{"id": post.id, **post.to_dict()} for post in posts_ref]
    return jsonify(posts), 200

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    filename = f"images/{uuid.uuid4()}.jpg"
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    image_url = blob.public_url
    return jsonify({'image_url': image_url}), 201

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    chat_id = f"{data['sender']}_{data['receiver']}"
    db.collection(f'chats/{chat_id}/messages').add({
        "sender": data['sender'],
        "message": data['message'],
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return jsonify({'message': 'Message sent'}), 201

if __name__ == '__main__':
    app.run(debug=True)
