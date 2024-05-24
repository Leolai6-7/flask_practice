#request_body
{
  "directory_path": "/path/to/directory",
  "file_names": ["example1.txt", "example2.txt"]
}


#response_body，file1為密件,file2非密件
{
  "results": [
    {
      "file_name": "file1.txt",
      "receipt_number": "收文編號",
      "receipt_date": "收文日期",
      "issuing_authority": "發文機關名稱",
      "issue_date": "發文日期",
      "issue_reference_number": "發文機關字號",
      "registration_number": "掛號號碼(若為電子公文則帶入電子公文)",
      "subject": "密 文件主旨",
      "classification": "密"
    },
    {
      "file_name": "file2.txt",
      "receipt_number": "收文編號",
      "receipt_date": "收文日期",
      "issuing_authority": "發文機關名稱",
      "issue_date": "發文日期",
      "issue_reference_number": "發文機關字號",
      "registration_number": "掛號號碼(若為電子公文則帶入電子公文)",
      "subject": "文件主旨",
      "classification": "一般"
    }
  ]
}

#main
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
api = Api(app)


class UploadFiles(Resource):
    def post(self):
        directory_path = request.form.get('directory_path')
        if not directory_path or not os.path.isdir(directory_path):
            return jsonify(self.create_error_response('Invalid directory path')), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify(self.create_error_response('No files provided')), 400
        
        results = []
        for file in files:
            file_name = secure_filename(file.filename)
            file_path = os.path.join(directory_path, file_name)
            try:
                file.save(file_path)
                file_result = self.process_file(file_path)
                file_result['error'] = None
            except Exception as e:
                file_result = self.create_file_error_response(file_name, str(e))
            results.append(file_result)
        
        return jsonify({'results': results})

    def create_error_response(self, error_message):
        return {
            'results': [
                {
                    'file_name': None,
                    'receipt_number': None,
                    'receipt_date': None,
                    'issuing_authority': None,
                    'issue_date': None,
                    'issue_reference_number': None,
                    'registration_number': None,
                    'subject': None,
                    'classification': None,
                    'error': error_message
                }
            ]
        }

    def create_file_error_response(self, file_name, error_message):
        return {
            'file_name': file_name,
            'receipt_number': None,
            'receipt_date': None,
            'issuing_authority': None,
            'issue_date': None,
            'issue_reference_number': None,
            'registration_number': None,
            'subject': None,
            'classification': None,
            'error': error_message
        }

    def process_file(self, file_path):
        pass

api.add_resource(ProcessFiles, '/process-files')

if __name__ == '__main__':
    app.run(debug=True)
    
    
