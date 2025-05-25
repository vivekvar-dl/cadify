import tempfile

from loguru import logger

from .agents import execute_python_code
from .chains import CadCodeGeneratorChain, CadCodeRefinerChain
from .image import ImageData
from .render import render_and_export_image


def index_map(index: int) -> str:
    if index == 0:
        return "1st"
    elif index == 1:
        return "2nd"
    elif index == 2:
        return "3rd"
    else:
        return f"{index + 1}th"

def generate_step_from_2d_cad_image(image_filepath: str, output_filepath: str, num_refinements: int = 3):
    """Generate a STEP file from a 2D CAD image

    Args:
        image_filepath (str): Path to the 2D CAD image
        output_filepath (str): Path to the output STEP file
    """
    image_data = ImageData.load_from_file(image_filepath)

    # Generate code to convert 2D CAD image to 3D CAD model using the 'cadquery' Python library
    # Export the generated 3D model as a STEP file using the `cadquery.exporters.export` function
    chain = CadCodeGeneratorChain()

    result: str = chain.invoke(image_data)["result"]
    code = result.format(output_filename=output_filepath) # Replace {output_filename} template with output_filepath
    logger.info("1st code generation complete. Running code...")
    logger.debug("Generated 1st code:")
    logger.debug(code)
    output = execute_python_code(code) # Have LLM agent modify the code to ensure it executes properly
    logger.debug(output)

    # Compare the 3D view image from the 3D CAD model with the 2D CAD image
    # and modify the code to improve the CAD model
    refiner_chain = CadCodeRefinerChain()

    # Perform code refinement num_refinements times
    for i in range(num_refinements):
        path = "tmp/render_and_export_image.png"
        render_and_export_image(output_filepath, path) # Convert 3D CAD model to 3D view image
        logger.info(f"Temporarily rendered image to {path}")
        rendered_image = ImageData.load_from_file(path)
        result = refiner_chain.invoke({
            "code": code, 
            "original_input": image_data, 
            "rendered_result": rendered_image,
            "rendered_image_type": rendered_image.type,
            "rendered_image_data": rendered_image.data,
            "original_image_data": image_data.data,
            "original_image_type": image_data.type
        })["result"]
        code = result.format(output_filename=output_filepath)
        logger.info("Refined code generation complete. Running code...")
        logger.debug(f"Generated {index_map(i)} refined code:")
        logger.debug(code)
        output = execute_python_code(code)
        logger.debug(output)
