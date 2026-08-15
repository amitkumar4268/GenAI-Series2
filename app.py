from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


module_path = Path(__file__).parent / "apps" / "5_pdf_qna_gradio.py"
spec = spec_from_file_location("pdf_qna_gradio", module_path)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load Gradio app module from apps/5_pdf_qna_gradio.py")

module = module_from_spec(spec)
spec.loader.exec_module(module)
demo = module.demo


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
