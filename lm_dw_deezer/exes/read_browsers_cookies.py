from sqlite3 import connect

# from secretstorage import (
# 	dbus_init, get_any_collection
# )

from .data_utils import home_user


FIREFOX_FILE = 'cookies.sqlite'
CHROME_FILE = 'Databases.db'


# MHH, DON'T ADD A FUNCTION FOR SENDING COOKIES TO YOUR SERVER! DON'T ADD A FUNCTION FOR SENDING COOKIES TO YOUR SERVER! DON'T ADD A FUNCTION FOR SENDING COOKIES TO YOUR SERVER! :)


def read_firefox() -> str | None:
	files = home_user.rglob(FIREFOX_FILE)
	arl = None

	for file in files:
		c_file = str(file.absolute())

		if (not 'firefox' in c_file) or ('crashrecovery' in c_file):
			continue
		
		db = connect(c_file)
		cursor = db.cursor()
		query = 'SELECT value FROM moz_cookies WHERE name = \'arl\' and host = \'.deezer.com\''
		cursor.execute(query)
		arl = cursor.fetchone()[0]
		cursor.close()
		db.close()

		break

	return arl


# def read_chrome() -> str | None:
# 	files = home_user.rglob(CHROME_FILE)
# 	arl = None
# 	conn = dbus_init()
# 	collection = get_any_collection(conn)

# 	for file in files:
# 		if 'microsoft-edge' in file.as_posix():
# 			for it in collection.get_all_items():
# 				print(it.get_attributes(), it.get_secret())

# 	return arl