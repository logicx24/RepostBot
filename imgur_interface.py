import pyimgur

class ImgurInterface(object):

	def __init__(self, imgur_instance):
		self.imgur_instance = imgur_instance

	def upload_image_from_url(self, url):
		output = self.imgur_instance.upload_image(url=url)
		if output:
			return output.link
		return None