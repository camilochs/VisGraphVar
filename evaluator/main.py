import yaml
from pathlib import Path
from visgraphvar.graph_generator import GraphGenerator
from tasks.detection.main import evaluation_detection
from tasks.classification.main import evaluation_classification
from tasks.segmentation.main import evaluation_segmentation
from tasks.link_prediction.main import evaluation_link_prediction
from tasks.pattern_recognition.main import evaluation_pattern_recognition
from tasks.reasoning.main import evaluation_reasoning
from tasks.matching.main import evaluation_matching
current_path = Path(__file__).resolve().parent

def load_config():
    with open(current_path /  'config.yaml') as f:
        data = yaml.safe_load(f)
    new_class = type("Config", (object,), data)
    return new_class

Config = load_config()
config = Config()


evaluation_detection(config.benchmark_path, config.models_availables, config.prompts_type, config.task_prompt_path["detection"])
#evaluation_classification(config.benchmark_path, config.models_availables, config.prompts_type, config.task_prompt_path["classification"])
#evaluation_segmentation(config.benchmark_path, config.models_availables, config.prompts_type, config.task_prompt_path["segmentation"])
#evaluation_link_prediction(config.benchmark_path, config.models_availables, config.prompts_type, config.task_prompt_path["link_prediction"])
#evaluation_pattern_recognition(config.benchmark_path, config.models_availables, config.prompts_type, config.task_prompt_path["pattern_recognition"])
#evaluation_matching(config.benchmark_path, config.models_availables, config.prompts_type, config.task_prompt_path["matching"])
#evaluation_reasoning(config.benchmark_path, config.models_availables, config.prompts_type, config.task_prompt_path["reasoning"])