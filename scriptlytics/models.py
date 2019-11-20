from django.db import models
import json
import time

class Software(models.Model):
    hit_list = models.TextField(default='[]')
    
    @property
    def hits(self):
        return json.loads(self.hit_list)
    
    @property
    def unique_hits(self):
        unique = []
        for hit in json.loads(self.hit_list):
            if hit['username'] not in [u['username'] for u in unique]:
                unique.append(hit)
        return unique
    
    @property
    def format_for_graph(self):
        formatted_data = ''
        unique_count = 0
        for i, hit in enumerate(self.hits):
            if hit in self.unique_hits:
                unique_count += 1
            formatted_data += '{},{},{}\n'.format(hit['timestamp'], i+1, unique_count)
        return formatted_data
            
    
    @property
    def num_times_ran(self):
        try:
            return round(len(self.hits) / len(self.unique_hits), 2)
        except ZeroDivisionError:
            return 'N/A'
    
    @property
    def usernames(self):
        return list(set([hit['username'] for hit in json.loads(self.hit_list)]))
    
    def hit(self, username):
        hit_list = json.loads(self.hit_list)
        hit_list.append({'timestamp': time.time(), 'username': username})
        self.hit_list = json.dumps(hit_list)
        self.save()