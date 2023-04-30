from flask import *
from pymongo import MongoClient
import os, gridfs, pymongo, time ##will add sendgrid and twilio functionality.
from werkzeug import secure_filename
from random import randint
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'
db = "share"

@app.route('/')
def home():
	if not os.path.exists('upload/'):
		try:
			os.makedirs('upload/')
		except Exception as e:
			print e
	    	raise Exception("SOMETHING WENT HORRIBLY WRONG. BREAKING.")
	return render_template('index.html')

# safety function to get a connection to the db above
def get_db():
	conn = None
	try:
	    conn = pymongo.MongoClient()
	except pymongo.errors.ConnectionFailure, e:
	   raise Exception("Could not connect to MongoDB: %s" % e)
	return conn[db]

# returns if space is taken
def search_file(room_number):
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	try:
		_id = db_conn.fs.files.find_one(dict(room = room_number))
	except Exception:
		_id = None
	if not _id:
		return False
	else:
		return True

#find a random integer not currently in the db
def find_number():
	while True:
		temp = randint(1,100) #inclusive
		if search_file(temp):
			continue
		else: ##we've found a random integer NOT already in the db, return
			return temp

# put files in mongodb
def insert_file(file_name, room_number):
	if not(file_name and room_number):
		return
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	if search_file(room_number):
		print "Space :"+str(room_number)+' is taken!'
		return False
	try:
		with open('upload/' + file_name, "r") as f:
			gfs.put(f, room=room_number)
		print "Stored file :"+str(room_number)+' Successfully'
		return True
	except Exception as e:
		print "File :"+'upload/'+file_name+" probably doesn't exist, : "+str(e)
		return False

# remove files from mongodb
def delete_file(room_number):
	if not(room_number):
		raise Exception("delete_file given None")
	if not search_file(room_number):
		print "File "+str(room_number)+' not in db, error?'
		return True
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	_id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
	gfs.delete(_id)
	print "Deleted file :"+str(room_number)+' Successfully'
	return True

def extract_file(output_location, room_number):
	if not(output_location and room_number):
		raise Exception("extract_file not given proper values")
	if not search_file(room_number):
# read files from mongodb
		print "File "+str(room_number)+' not in db, error?'
		return False
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	try:
		_id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
		with open('upload/' + str(room_number) , 'w') as f:
			f.write(gfs.get(_id).read())
		gfs.get(_id).read()
		print "Written file :"+str(room_number)+' Successfully'
		return True
	except Exception as e:
		print "failed to read file :"+str(e)
		return False

#upload routine
@app.route('/upload',methods=['POST'])
def upload():
	#get the form inputs
	file = request.files['file']
	space = request.form['space']
	# if file and space are given
	if file and space:
		# search to see if number is taken
		if search_file(space):
			#space is taken, generate new available number
			new = find_number()
			render_template('index.html', space=space, new=new)
		#make the file safe, remove unsupported chars
		filename = secure_filename(file.filename)
		#move the file to our upload folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		# save file to mongodb
		res = insert_file(filename,space)
		# upload failed for whatever reason
		if not res:
			os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , filename ))
			return render_template('index.html', space=space, failed=True)
		if app.debug:
			# debugging lines to write a record of inserts
			with open('debug.txt', 'w') as f:
				f.write('File name is :'+filename+', and the space is :'+ str(space))
		# file upload successful, remove copy from disk.
		os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] ,  filename  ))
		return render_template('index.html', space=space, upload=True)
	else:
		return render_template('invalid.html')
	@after_this_request
	def expire_file():
		time.sleep(600)
		delete_file(space)
		os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , str( space )))
		return

@app.route('/upload/<spacenum>', methods=['GET'])
def download(spacenum):
	unSecurefilename = extract_file(app.config['UPLOAD_FOLDER'] ,spacenum )
	render_template('index.html' , spacenum = spacenum)
	return send_from_directory(app.config['UPLOAD_FOLDER'], str(spacenum) )
	@after_this_request
	def clean_File(response):
		print 'Response is : '+response
		os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , str( spacenum )))
		return

@app.errorhandler(404)
def new_page(error):
	if app.debug:
		raise Exception("404 ERROR!!")
		#For debugging!!
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)
