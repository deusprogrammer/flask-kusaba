from models import User

def authenticate_user(username, password):
	print "SEARCHING FOR USER %s", username
	user = User.query.filter_by(username=username)
	if user.count() == 0:
		print "NO SUCH USER"
		return None
		
	user = user.one()
	
	# Replace this with a hashing scheme
	if user.password == password:
		print "ACCESS GRANTED"
		user.authenticated = True
		return user
	else:
		print "ACCESS DENIED"
		user.authenticated = False
		return user