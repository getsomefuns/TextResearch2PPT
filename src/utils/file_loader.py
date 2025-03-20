# src/utils/config_manager.py
class PipelineController:
    def __init__(self, config_path="workflows/custom_process.json"):
        self.steps = self._load_config(config_path)
        
    def execute(self, user_input):
        if "text_generation" in self.steps:
            research_data = ResearchAgent().generate(user_input)
            save_json(research_data, "intermediate/research_output.json")
            
        if "mindmap_generation" in self.steps:
            if not os.path.exists("intermediate/research_output.json"):
                raise FileNotFoundError("需要先执行文本生成阶段")
            modified_text = self._check_modification("intermediate/research_output.json")
            MindmapEngine().generate(modified_text)
            
        if "ppt_generation" in self.steps:
            mindmap_path = self._get_latest_mindmap()
            PPTBuilder().convert(mindmap_path)