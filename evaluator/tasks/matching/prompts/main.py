import os
import itertools
from pathlib import Path
from utils.llm import execute_llm 
from utils.manage_file import read_prompt, write_result_llm

current_path = Path(__file__).resolve().parent

def execute(model_name, prompt, path_image):
    return execute_llm(model_name, prompt, path_image)

def evaluation_pattern_recognition(benchmark_path, models, prompts_type, template_prompts):
    task = "pattern_recognition"
    total_executions = 0
    prompt = {}
    task_benchmark_path = os.path.join(benchmark_path, task)
    print(task_benchmark_path)
    for root_folder, _, files in os.walk(task_benchmark_path):
        for file in sorted(files):
            if ".png" in file:
                for model_name, prompt_type in itertools.product(models, prompts_type):
                    folder_benchmarks = root_folder.replace(f"{benchmark_path}{task}/", "" )
                    path_model = os.path.join(current_path.as_posix(), "evaluations", folder_benchmarks, "results", model_name.split("/")[-1], prompt_type)
                    if not os.path.exists(path_model):
                        Path(path_model).mkdir(parents=True, exist_ok=True)
                
                    path_model = os.path.join(current_path.as_posix(), "evaluations", folder_benchmarks, "results", model_name.split("/")[-1], prompt_type)
                    path_image = os.path.join(root_folder, file)
                    path_prompt = os.path.join(current_path.as_posix(), template_prompts[prompt_type])
                    
                    if path_prompt not in prompt:
                        prompt[path_prompt] = read_prompt(path_prompt)
                    
                    path_result_model = os.path.join(path_model, file.replace(".png", ".txt"))
                    if not os.path.exists(path_result_model):
                        print(f"Beginned: {path_result_model}")

                        output_llm = execute(model_name, prompt[path_prompt], path_image)
                        if not output_llm:
                            return
                        
                        write_result_llm(path_result_model, output_llm)
                        print(f"Finished: {path_result_model}")
                        total_executions += 1

    print(f"Finished: {total_executions} executions.")