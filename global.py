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
import json

app = Flask(__name__)
api = Api(app)

class ProcessFiles(Resource):
    def post(self):
        data = request.get_json()
        directory_path = data.get('directory_path')
        file_names = data.get('file_names')
        
        if not directory_path or not os.path.isdir(directory_path):
            return {'error': 'Invalid directory path'}, 400
        
        if not file_names or not isinstance(file_names, list):
            return {'error': 'Invalid file names'}, 400
        
        results = []
        for file_name in file_names:
            file_path = os.path.join(directory_path, file_name)
            if not os.path.isfile(file_path):
                results.append({
                    'file_name': file_name,
                    'error': 'File not found'
                })
            else:
                file_result = self.process_file(file_path)
                results.append(file_result)
        
        return jsonify({'results': results})

    def process_file(self, file_path):
        pass

api.add_resource(ProcessFiles, '/process-files')

if __name__ == '__main__':
    app.run(debug=True)