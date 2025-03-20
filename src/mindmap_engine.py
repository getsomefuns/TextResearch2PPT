import subprocess
import tempfile

class MindmapGenerator:
    def generate_from_json(self, json_data, output_path):
        # 转换为Mermaid语法
        mmd_content = "graph TD\n"
        for section in json_data["sections"]:
            mmd_content += f"  {json_data['title']} --> {section['title']}\n"
            for point in section["points"]:
                mmd_content += f"  {section['title']} --> {point}\n"
        
        # 生成临时文件
        with tempfile.NamedTemporaryFile(suffix=".mmd", delete=False) as f:
            f.write(mmd_content.encode('utf-8'))
            temp_path = f.name
        
        # 调用Mermaid CLI
        subprocess.run(["mmdc", "-i", temp_path, "-o", output_path])