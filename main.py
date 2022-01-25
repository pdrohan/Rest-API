# from typing_extensions import Required
from email import message
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes = {likes})"

# we only want to run this once
# db.create_all()



video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="likes of the video is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="views of the video is required")
video_update_args.add_argument("likes", type=int, help="likes of the video is required")


resouce_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,
}

# def abort_if_vid_id_dn_exist(video_id):
#     if video_id not in videos:
#         abort(404, message="Could not find video...")
    
# def abort_if_vid_exists(video_id):
#     if video_id in videos:
#         abort(409, message="Video already exists with that ID...")

#Serializeable 
'''
Dictionaries follow json format,
because we are returning json serializeable objects
'''
class Video(Resource):
    @marshal_with(resouce_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='could not find video with that id')
        return result
    
    
    @marshal_with(resouce_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message='Video id Taken')
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    # I feel like there is a better way to do this 
    @marshal_with(resouce_fields)
    def patch(self,video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Video does not exist, cannot update')

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        db.session.commit()
        return result



    def delete(self, video_id):
        abort_if_vid_id_dn_exist(video_id)
        del videos[video_id]
        return '', 204




api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)