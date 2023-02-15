from flask import *
from pymongo import MongoClient
import sys,os,sendgrid,twilio, gridfs,pymongo  ##will add sendgrid and twilio functionality.
from werkzeug import secure_filename
##ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
db = "fileflow"
url_rule = None

def get_db(): # get a connection to the db above
	conn = None
	try:
	    conn = pymongo.MongoClient()
	except pymongo.errors.ConnectionFailure, e:
	   print "Could not connect to MongoDB: %s" % e
	   sys.exit(1)
	return conn[db]

# put files in mongodb
def put_file(file_name, room_number):
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	with open('uploads/' + file_name, "r") as f:
		gfs.put(f, room=room_number)

# read files from mongodb
def read_file(output_location, room_number):
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	_id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
	#return gfs.get(_id).read()
	with open(output_location, 'w') as f:
		f.write(gfs.get(_id).read())

@app.route('/')
def home():
	return render_template('index.html')


@app.route('/upload',methods=['POST'])
def upload():
	#get the name of the uploaded file
	file=request.files['file']
	#print "requested files"
	space=request.form['space']
	# if the file exists make it secure
	if file and space: #if the file exists
		#make the file same, remove unssopurted chars
		filename=secure_filename(file.filename)
		#move the file to our uploads folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		put_file(filename,space)
		# remove the file from disk as we don't need it anymore after database insert.
		os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , filename))
		# maybe redirect user to the uploaded_file route, which will show the uploaded file.
		return render_template('index.html', filename = filename ,space = space) ##take the file name
	else:
		return render_template('invalid.html')


@app.route('/uploads/<spacenum>', methods=['GET'])
def return_file(spacenum):
	print app.config['UPLOAD_FOLDER']
	## print filename= something
	read_file(app.config['UPLOAD_FOLDER'] ,spacenum)
	send_from_directory(app.config['UPLOAD_FOLDER'], filename)
	return render_template('thanks.html' , spacenum = spacenum)


@app.errorhandler(404)
def new_page(error):
	'''
	pagepath = request.path.lstrip('/')
	if pagepath.startswith('uploads'):
        	filename = pagepath[len('uploads'):].lstrip('/')
        	return render_template('upload.html', filename=filename)
    	else:
        	return render_template('edit.html', page=None, pagepath=pagepath)
	'''
	return render_template('error.html')
if __name__ == '__main__':
	app.run(debug=True)
	''' i have no recollection of why these are below
	file_location = "/Users/bedrich/Desktop/TODO-MCI"
	output_location = "/Users/bedrich/Desktop/omg"
	room_number = 12
	#put_file(file_location, room_number)
	#read_file(output_location, room_number)
	'''
