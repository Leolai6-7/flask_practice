#request_body
{
  "directory_path": "/path/to/directory"
}
#response_body
{
  "results": [
    {
      "file_name": "file1.txt",
      "receipt_number": "12345",
      "receipt_date": "2024-01-01",
      "issuing_authority": "某机关",
      "issue_date": "2024-01-02",
      "issue_reference_number": "XYZ-2024-001",
      "registration_number": "电子公文",
      "subject": "密 某文件主旨",
      "classification": "密"
    },
    {
      "file_name": "file2.txt",
      "receipt_number": "67890",
      "receipt_date": "2024-02-01",
      "issuing_authority": "另一个机关",
      "issue_date": "2024-02-02",
      "issue_reference_number": "ABC-2024-002",
      "registration_number": "123456789",
      "subject": "另一个文件主旨",
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
        
        if not directory_path or not os.path.isdir(directory_path):
            return {'error': 'Invalid directory path'}, 400

        results = []
        
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                file_result = self.process_file(file_path)
                results.append(file_result)
        
        return jsonify({'results': results})

    def process_file(self, file_path):
        # 示例分析逻辑，需根据实际文件格式实现
        with open(file_path, 'r') as file:
            content = file.read()
            # 以下为模拟解析结果，请根据实际需求替换解析逻辑
            parsed_data = {
                "receipt_number": "12345",
                "receipt_date": "2024-01-01",
                "issuing_authority": "某机关",
                "issue_date": "2024-01-02",
                "issue_reference_number": "XYZ-2024-001",
                "registration_number": "电子公文",  # 若为电子公文，则设为"电子公文"
                "subject": "某文件主旨",
                "classification": "密"
            }
            # 如果密等为"密"，在主旨前添加"密"
            if parsed_data["classification"] == "密":
                parsed_data["subject"] = "密 " + parsed_data["subject"]
        
        parsed_data["file_name"] = os.path.basename(file_path)
        return parsed_data

api.add_resource(ProcessFiles, '/process-files')

if __name__ == '__main__':
    app.run(debug=True)

