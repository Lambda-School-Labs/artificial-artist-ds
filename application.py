import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from helper import check_entry, generate_and_save


def create_app():
	application = Flask(__name__)
	CORS(application)

	@application.route('/')
	def root():
		return "Index; nothing to see here."

	@application.route('/entry', methods=['GET', 'POST'])
	def check_url():

		if request.method == 'POST':
			reqs = request.get_json()

			preview = reqs['preview']
			video_id = reqs['video_id']
			
			#default values initiated
			resolution = '128'
			im_group = None
			jitter = 0.5
			depth = 1
			truncation = 0.5

			#checks to see if other values are specified by user
			if 'resolution' in reqs:
				resolution = reqs['resolution']
			
			if 'im_group' in reqs:
				im_group = reqs['im_group']
			
			if 'jitter' in reqs:
				jitter = reqs['jitter']
			
			if 'depth' in reqs:
				depth = reqs['depth']
			
			if 'truncation' in reqs:
				truncation = reqs['truncation']

			return check_entry(preview, video_id, resolution, im_group, jitter, 
								depth, truncation)

		preview = str(request.args.get('preview'))
		video_id = str(request.args.get('video_id'))
		
		resolution = request.args.get('resolution')
		if resolution != None:
			resolution = str(resolution)
		
		im_group = request.args.get('im_group')
		if im_group != None:
			im_group = str(im_group)
		
		jitter = request.args.get('jitter')
		if jitter == None:
			jitter = 0.5
		
		depth = request.args.get('depth')
		if depth == None:
			depth = 1
		
		truncation = request.args.get('truncation')
		if truncation == None:
			truncation = 0.5
		
		return check_entry(preview, video_id, resolution, im_group, jitter, 
							depth, truncation)

	@application.route('/visualize', methods=['GET', 'POST'])
	def visual():

		if request.method == 'POST':
			reqs = request.get_json()

			preview = reqs['preview']
			video_id = reqs['video_id']
			resolution = reqs['resolution']
			classes = reqs['classes']
			jitter = reqs['jitter']
			depth = reqs['depth']
			truncation = reqs['truncation']

			return generate_and_save(preview, video_id, resolution, classes,
										jitter, depth, truncation)

		preview = str(request.args.get('preview'))
		video_id = str(request.args.get('video_id'))
		resolution = str(request.args.get('resolution'))
		classes = str(request.args.get('classes'))
		jitter = request.args.get('jitter')
		depth = request.args.get('depth')
		truncation = request.args.get('truncation')

		return generate_and_save(preview, video_id, resolution, classes,
									jitter, depth, truncation)

	return application