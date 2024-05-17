from flask import Blueprint
from src.database.models import Form
from src.database import db
import numpy as np 


api_reports_blueprint = Blueprint('api_reports_controller', __name__)

@api_reports_blueprint.get('/api/reports/<int:form_id>')
def index(form_id):
	# Extrae el formulario con su llave primaria.
	# No olvides checar si es None y regresar un 404 
	# con return tu_json_con_el_mensaje_de_error, 404
	form = db.session.get(Form, form_id)
	response_analysis_dict = {}
	if form is None:
		response_analysis_dict['Error msg:'] = '404'
	else:
		#this chunk code extracts a list of lists with the scores for each response of the form 
		responses_list = form.responses
		response_elements_list = []
		list_of_scores_for_each_response = []
		for response in responses_list:
			response_elements_list = response.data
			scores = []
			for item in response_elements_list:
				question_type = item['type']
				question_type = question_type.split('[')[0]
				if question_type == 'selection':
					scores.append(float(item['response']['score']))
			list_of_scores_for_each_response.append(scores)
			print(list_of_scores_for_each_response)
		#creating another list to calculate and map the np.mean() of the responses from each response
		#in order to calculate the average risk from all the responses registered for that form
		#primero eliminamos las sublistas vacias (preguntas que no son del tipo selection)
		average_score_from_each_response = [np.mean(element) for element in list_of_scores_for_each_response]
		form_average_risk = np.mean(average_score_from_each_response)
		response_analysis_dict['average_risk_from_all_responses'] = form_average_risk
		if form_average_risk <= 0.3:
			conclusion = 'El nivel de riesgo es bajo'
		elif form_average_risk > 0.3 <= 0.8:
			conclusion = 'Existe un nivel de riesgo medio'
		else: conclusion = 'Existe un nivel de riesgo ALTO!!'
		response_analysis_dict['conclusion'] = conclusion
		response_analysis_dict['average_score_from_each_response'] = average_score_from_each_response
		possible_responses = [0.0,0.3,0.6,1.0]
		counts = {element: 0 for element in possible_responses}
		for sublist in list_of_scores_for_each_response:
			for element in sublist:
				if element in counts:
					counts[element] += 1
		response_analysis_dict['qty_of_responses_of_each_risk'] = counts
		print(response_analysis_dict)
	return response_analysis_dict
		
		

			
			
        
			
				
    

