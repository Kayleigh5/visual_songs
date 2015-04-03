lyrics_array = []

class LyricsSearchPipeline(object):
    def process_item(self, item, spider):
    	global lyrics_array
    	lyrics_array.append(item)