from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
api= Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite.db'
db=SQLAlchemy(app)

class model(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.String(10))
    name=db.Column(db.String(200))
    branch=db.Column(db.String(200))
    college=db.Column(db.String(200))
    batch=db.Column(db.String(200))
    course=db.Column(db.String(200))
    first_language=db.Column(db.String(500))

#db.create_all()

postArgs=reqparse.RequestParser()

postArgs.add_argument("student_id",type=str,help="student_id is required",required=True)
postArgs.add_argument("name",type=str,help="name is required",required=True)
postArgs.add_argument("branch",type=str,help="branch is required",required=True)
postArgs.add_argument("college",type=str,help="college is required",required=True)
postArgs.add_argument("batch",type=str,help="batch is required",required=True)
postArgs.add_argument("course",type=str,help="course is required",required=True)
postArgs.add_argument("first_language",type=str,help="first_language is required",required=True)


resource_fields= { 'id': fields.Integer,'student_id': fields.String, 'name':fields.String, 'branch':fields.String, 'college':fields.String, 'batch':fields.String, 'course':fields.String, 'first_language':fields.String}

class allClass(Resource):
    def get(self):
        tt=model.query.all()
        s={}
        for entry in tt:
            s[entry.id]={"student_id":entry.student_id, "name":entry.name, "branch":entry.branch,"college":entry.college,"batch":entry.batch,"course":entry.course,"first_language":entry.first_language}
        return s

class students(Resource):
    @marshal_with(resource_fields)
    def get(self,todo_id):
        entry=model.query.filter_by(id=todo_id).first()
        if not entry:
            abort(404, message="No entry available with that ID")	
        return entry
    
    @marshal_with(resource_fields)
    def post(self,todo_id):
        args=postArgs.parse_args()
        entry=model.query.filter_by(id=todo_id).first()
        if entry:
            abort(409,message="ID used")
        
        todo=model(id=todo_id, student_id=args['student_id'],name=args['name'], branch=args['branch'], college=args['college'], batch=args['batch'], course=args['course'], first_language=args['first_language'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201
    
    def delete(self,todo_id):
        entry=model.query.filter_by(id=todo_id).first()
        db.session.delete(entry)
        return 'Student Deleted', 204

api.add_resource(allClass, '/mcit/cst-students/all')
api.add_resource(students, '/mcit/cst-students/all/<int:todo_id>') 
 
if __name__ == '__main__':
    app.run(debug=True)
