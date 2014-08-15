class RiakImage:
    def __init__(self, img_binary, meta):
        self.img_binary = img_binary
        self.mime_type = meta['mimeType']
        self.width = meta['width']
        self.height = meta['height']
        self.size = meta['size']
        self.id = meta['id']
        self.title = meta['title']