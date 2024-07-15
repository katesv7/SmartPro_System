from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

class Feedback:
    def __init__(self, student_id, rating, comment):
        self.student_id = student_id
        self.rating = rating
        self.comment = comment
        self.date = datetime.datetime.now()

class PracticalElement:
    def __init__(self, name):
        self.name = name
        self.feedback_list = []

    def add_feedback(self, feedback):
        self.feedback_list.append(feedback)

class System:
    def __init__(self):
        self.elements = {
            'project1': PracticalElement('project1'),
            'project2': PracticalElement('project2'),
            # Add predefined practical elements here
        }

    def submit_feedback(self, student_id, element_name, rating, comment):
        if element_name in self.elements:
            feedback = Feedback(student_id, rating, comment)
            self.elements[element_name].add_feedback(feedback)
        else:
            raise ValueError("Practical element not found")

    def view_feedback(self, element_name):
        if element_name in self.elements:
            return self.elements[element_name].feedback_list
        else:
            raise ValueError("Practical element not found")

    def generate_report(self):
        report = {}
        for element in self.elements.values():
            report[element.name] = {
                'total_feedbacks': len(element.feedback_list),
                'average_rating': self.calculate_average_rating(element.feedback_list)
            }
        return report

    @staticmethod
    def calculate_average_rating(feedback_list):
        if not feedback_list:
            return 0
        total_rating = sum(feedback.rating for feedback in feedback_list)
        return total_rating / len(feedback_list)

system = System()

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        student_id = request.json['student_id']
        element_name = request.json['element_name']
        rating = int(request.json['rating'])
        comment = request.json['comment']
        system.submit_feedback(student_id, element_name, rating, comment)
        return jsonify({"message": "Feedback submitted successfully."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/view_feedback', methods=['GET'])
def view_feedback():
    try:
        element_name = request.args.get('element_name')
        feedbacks = system.view_feedback(element_name)
        feedback_list = [{
            'student_id': feedback.student_id,
            'rating': feedback.rating,
            'comment': feedback.comment,
            'date': feedback.date.strftime('%Y-%m-%d %H:%M:%S')
        } for feedback in feedbacks]
        return jsonify(feedback_list)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/generate_report', methods=['GET'])
def generate_report():
    report = system.generate_report()
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True)
